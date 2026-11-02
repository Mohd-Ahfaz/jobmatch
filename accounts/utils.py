import asyncio
import concurrent.futures
import os
import re

from django.conf import settings
from PIL import Image
from pypdf import PdfReader

# winocr is Windows-only. Import gracefully so the app works on Linux (Render).
try:
    import winocr
    _WINOCR_AVAILABLE = True
except ImportError:
    _WINOCR_AVAILABLE = False

from .models import Profile, Skill, UserSkill

EDUCATION_PATTERN = r"\b(b\.?tech|m\.?tech|bachelor|master of|diploma|bca|mca|b\.?sc|m\.?sc|b\.e|m\.e|ph\.?d|bba|mba|degree)\b"
EXPERIENCE_HEADINGS = [
    "experience", "work experience", "professional experience",
    "internship", "internships", "projects", "work history", "employment history"
]
STOP_HEADINGS = [
    "education", "skills", "technical skills", "certifications",
    "achievements", "languages", "hobbies", "declaration", "interests", "awards"
]
IGNORE_NAME_WORDS = {
    "resume", "curriculum", "vitae", "cv", "profile", "contact", "email",
    "phone", "address", "page", "portfolio", "github", "linkedin", "summary",
    "objective", "skills", "education", "experience", "declaration", "software",
    "engineer", "developer", "designer", "intern", "manager", "analyst", "student"
}


def get_profile(user):
    return Profile.objects.get_or_create(user=user)[0]


def save_skills(user, skills):
    UserSkill.objects.filter(user=user).exclude(skill__in=skills).delete()
    for skill in skills:
        UserSkill.objects.get_or_create(user=user, skill=skill)


def ocr_pil_image(img):
    """
    Extracts text from a PIL Image using Gemini Vision if configured,
    or the high-performance native Windows Media OCR engine (offline).
    """
    # 1. Try Gemini Vision if API key is present
    api_key = getattr(settings, "GEMINI_API_KEY", "")
    if api_key:
        try:
            import base64
            import io
            import json
            import urllib.request
            buf = io.BytesIO()
            img.convert("RGB").save(buf, format="JPEG", quality=90)
            b64_data = base64.b64encode(buf.getvalue()).decode("utf-8")
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            payload = {
                "contents": [{
                    "parts": [
                        {"text": "Extract all text from this resume document accurately, preserving lines and sections."},
                        {"inlineData": {"mimeType": "image/jpeg", "data": b64_data}}
                    ]
                }]
            }
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                if len(text) > 30:
                    return text
        except Exception:
            pass

    # 2. Native Windows OCR engine (fast, offline, works for all image formats)
    if _WINOCR_AVAILABLE:
        try:
            async def _run():
                return await winocr.recognize_pil(img)

            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            if loop.is_running():
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    res = executor.submit(asyncio.run, _run()).result()
            else:
                res = loop.run_until_complete(_run())

            return getattr(res, "text", "") or ""
        except Exception:
            pass

    return ""


def extract_text_from_pdf(pdf_path):
    """
    Extracts text from all Adobe Acrobat and PDF formats:
    - Standard text PDFs
    - Acrobat layout mode (handles complex multi-column documents)
    - Acrobat AcroForms (interactive form fields)
    - Password-protected / encrypted Acrobat PDFs (empty user password)
    - Scanned Acrobat PDFs (extracts embedded page images and runs OCR)
    """
    text_chunks = []
    try:
        reader = PdfReader(pdf_path)
        if getattr(reader, "is_encrypted", False):
            try:
                reader.decrypt("")
            except Exception:
                pass

        # 1. Page text with layout preservation
        for page in reader.pages:
            try:
                page_text = page.extract_text(extraction_mode="layout") or ""
            except Exception:
                page_text = page.extract_text() or ""
            if page_text:
                text_chunks.append(page_text)

        # 2. Form fields (Adobe Acrobat interactive forms)
        try:
            fields = reader.get_form_text_fields()
            if fields:
                field_text = "\n".join(str(val) for val in fields.values() if val)
                if field_text:
                    text_chunks.append(field_text)
        except Exception:
            pass

        full_text = "\n".join(text_chunks).strip()

        # 3. Scanned PDF fallback: If text stream is empty or under 40 characters, OCR the page images
        if len(full_text) < 40:
            scanned_chunks = []
            for page in reader.pages:
                try:
                    for img_obj in page.images:
                        try:
                            ocr_text = ocr_pil_image(img_obj.image)
                            if ocr_text:
                                scanned_chunks.append(ocr_text)
                        except Exception:
                            continue
                except Exception:
                    continue
            if scanned_chunks:
                full_text = "\n".join(scanned_chunks).strip()

        return full_text
    except Exception:
        # Fallback: try opening with PIL in case a file named .pdf was actually an image
        try:
            img = Image.open(pdf_path)
            return ocr_pil_image(img)
        except Exception:
            return ""


def read_resume(profile):
    """
    Extracts text from any uploaded resume:
    - Photo / image formats: PNG, JPG, JPEG, WEBP, BMP, TIFF
    - All Adobe Acrobat & PDF formats: standard, multi-column, AcroForm, or scanned image PDF
    """
    if not profile or not profile.resume_file:
        return ""
    try:
        path = profile.resume_file.path
        if not os.path.exists(path):
            return ""

        lower_path = path.lower()
        image_exts = (".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff", ".tif", ".jfif")

        if lower_path.endswith(image_exts):
            img = Image.open(path)
            return ocr_pil_image(img)

        # Otherwise treat as PDF (Adobe Acrobat, standard, or scanned)
        text = extract_text_from_pdf(path)
        if not text:
            # Last resort: try PIL if PDF parsing failed
            try:
                img = Image.open(path)
                return ocr_pil_image(img)
            except Exception:
                pass
        return text or ""
    except Exception:
        return ""


def extract_name_from_text(lines):
    """Extracts candidate name from the top lines of the resume text."""
    for line in lines[:8]:
        cleaned = line.strip()
        if not cleaned:
            continue
        # Skip lines with email, URL, phone number, digits or delimiters
        if "@" in cleaned or "http" in cleaned.lower() or "www." in cleaned.lower() or "github" in cleaned.lower() or "linkedin" in cleaned.lower():
            continue
        if any(char.isdigit() for char in cleaned):
            continue
        if ":" in cleaned or "|" in cleaned or "/" in cleaned or "\\" in cleaned:
            continue

        words = cleaned.split()
        if 1 <= len(words) <= 4:
            all_alpha = all(w.replace(".", "").replace("-", "").isalpha() for w in words)
            not_ignored = not any(w.lower() in IGNORE_NAME_WORDS for w in words)
            if all_alpha and not_ignored and 2 < len(cleaned) <= 40:
                return cleaned.title()
    return ""


def fill_from_resume(profile):
    """
    Scans the uploaded resume PDF to extract:
    1. Name
    2. Education
    3. Experience
    4. Skills
    Returns a dictionary of extracted items.
    """
    text = read_resume(profile)
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    # 1. Scan Name
    extracted_name = extract_name_from_text(lines)
    if extracted_name and not profile.full_name:
        profile.full_name = extracted_name

    # 2. Scan Education
    if not profile.education:
        for line in lines:
            if re.search(EDUCATION_PATTERN, line, re.I):
                profile.education = line[:200].strip()
                break

    # 3. Scan Experience
    if not profile.experience:
        for i, line in enumerate(lines):
            line_clean = line.lower().strip(" :-\t")
            if any(h == line_clean or line_clean.startswith(h) for h in EXPERIENCE_HEADINGS):
                exp_lines = []
                for exp_line in lines[i + 1:]:
                    exp_clean = exp_line.lower().strip(" :-\t")
                    if any(s == exp_clean or exp_clean.startswith(s) for s in STOP_HEADINGS):
                        break
                    if exp_line.strip():
                        exp_lines.append(exp_line.strip())
                    if len(exp_lines) >= 8:
                        break
                if exp_lines:
                    profile.experience = "\n".join(exp_lines)
                break

    # 4. Scan Skills
    found = [s for s in Skill.objects.all() if re.search(r"\b" + re.escape(s.name) + r"\b", text, re.I)]
    for skill in found:
        UserSkill.objects.get_or_create(user=profile.user, skill=skill)

    profile.save()

    return {
        "name": profile.full_name,
        "education": profile.education,
        "experience": profile.experience,
        "skills": [s.name for s in found],
    }
