from datetime import date, timedelta
from urllib.parse import quote, urlencode

from django.conf import settings

from jobs.utils import my_skills

from .models import Application


def reminders_for(user):
    soon = date.today() + timedelta(days=2)
    return Application.objects.filter(
        user=user,
        status__in=["applied", "interview"],
        follow_up_on__isnull=False,
        follow_up_on__lte=soon,
    ).select_related("job").order_by("follow_up_on")


def mail_link(to, subject, body):
    if not to or "@" not in to or "example.com" in to:
        return ""
    return f"mailto:{to}?subject={quote(subject)}&body={quote(body)}"


def gmail_compose_link(to, subject, body):
    """
    Generate a direct Gmail web compose URL.
    Opens Gmail in the browser with recipient, subject, and pre-filled message body.
    Works reliably on Windows, Mac, and mobile without needing a desktop mail app.
    """
    if not to or "@" not in to or "example.com" in to:
        return ""
    params = {
        "view": "cm",
        "fs": "1",
        "to": to,
        "su": subject,
        "body": body,
    }
    return f"https://mail.google.com/mail/?{urlencode(params)}"


def make_resume(user, profile, job):
    owned = my_skills(user)
    required = [skill.name for skill in job.skills.all()]
    skills = [name for name in required if name in owned] + [name for name in owned if name not in required]
    focus = ", ".join(skills[:4]) or "software engineering"
    return (
        f"{profile.full_name or user.username}\n"
        f"{user.email} | {profile.city or 'Remote'}\n\n"
        f"PROFESSIONAL OBJECTIVE\n"
        f"Results-driven software engineer seeking the {job.title} position at {job.company}. "
        f"Bringing practical expertise in {focus} to deliver reliable, high-impact features.\n\n"
        f"CORE TECHNICAL SKILLS\n{', '.join(skills)}\n\n"
        f"EDUCATION\n{profile.education or 'Bachelor of Technology / Computer Science'}\n\n"
        f"EXPERIENCE & PROJECTS\n{profile.experience or 'Developed scalable web applications and completed verified skill assessments.'}\n"
    )


def make_cover_letter(user, profile, job):
    owned = my_skills(user)
    matched = [skill.name for skill in job.skills.all() if skill.name in owned]
    skills = ", ".join(matched) if matched else "modern software development tools"
    return (
        f"Dear Hiring Team at {job.company},\n\n"
        f"I am writing to express my strong enthusiasm for the {job.title} role. With hands-on experience "
        f"in {skills}, I am confident in my ability to hit the ground running and contribute to your engineering goals.\n\n"
        f"I have built projects demonstrating clean code architecture, problem-solving, and cross-functional collaboration. "
        f"I would welcome the opportunity to discuss how my background aligns with your team's needs.\n\n"
        f"Thank you for your time and consideration.\n\n"
        f"Sincerely,\n{profile.full_name or user.username}\n{user.email}"
    )


def ats_check(text, job):
    text_lower = text.lower()
    required = [skill.name for skill in job.skills.all()]
    found = [name for name in required if name.lower() in text_lower]
    missing = [name for name in required if name not in found]
    score = round(len(found) / len(required) * 100) if required else 100

    tips = []
    for section in ["skills", "education", "experience"]:
        if section not in text_lower:
            tips.append(f"Add a clear '{section.title()}' heading")
    words = len(text.split())
    if words < 100:
        notes = "Your resume text is brief. Add more specifics about project architecture and contributions."
        tips.append(notes)
    elif words > 800:
        tips.append("Resume exceeds recommended one-to-two page length. Aim for concise bullet points.")
    if "@" not in text:
        tips.append("Add a direct contact email address in your header")
    return {"score": score, "found": found, "missing": missing, "tips": tips}


import json
import re
import urllib.request


def interview_questions(job):
    """
    Generate role-specific, diverse interview questions tailored to the job's
    title, company, required technical skills, and seniority level.
    Covers architecture, production troubleshooting, system design, STAR behavioral,
    and strategic company alignment.
    """
    skills = [s.name for s in job.skills.all()]
    title = (job.title or "Software Engineer").strip()
    company = (job.company or "the company").strip()
    level = getattr(job, "level", "mid") or "mid"

    questions = []

    primary_skill = skills[0] if skills else None
    secondary_skill = skills[1] if len(skills) > 1 else None

    # 1. Technical Architecture & Core Stack Deep-Dive
    if primary_skill:
        p_lower = primary_skill.lower()
        if any(w in p_lower for w in ["python", "django", "fastapi", "flask"]):
            questions.append(
                f"In production {primary_skill} systems, how do you manage concurrency, asynchronous task workers (e.g. Celery or asyncio), and database query optimization like avoiding N+1 queries?"
            )
        elif any(w in p_lower for w in ["react", "javascript", "typescript", "next", "vue", "angular"]):
            questions.append(
                f"In high-traffic {primary_skill} applications, how do you handle complex state management, bundle size optimization, and client-side caching to prevent unnecessary component re-renders?"
            )
        elif any(w in p_lower for w in ["sql", "postgres", "mysql", "database", "mongo", "redis"]):
            questions.append(
                f"When architecting high-throughput data models in {primary_skill}, how do you evaluate indexing strategies, connection pooling, and cache invalidation policies?"
            )
        elif any(w in p_lower for w in ["docker", "kubernetes", "aws", "cloud", "devops", "ci/cd", "terraform"]):
            questions.append(
                f"Walk me through how you architect an automated, zero-downtime deployment pipeline using {primary_skill}, including rollback strategies and environment secret management."
            )
        elif any(w in p_lower for w in ["machine learning", "deep learning", "ai", "tensorflow", "pytorch", "pandas", "data"]):
            questions.append(
                f"How do you monitor for model/data drift in production, design reliable feature-engineering pipelines, and evaluate the trade-off between inference latency and model accuracy using {primary_skill}?"
            )
        else:
            questions.append(
                f"How have you architected and scaled a core component using {primary_skill}, and what critical design trade-offs did you make?"
            )
    else:
        questions.append(
            f"Walk me through the architecture of the most technically challenging software system you have built or maintained for the {title} role."
        )

    # 2. Production Incident & Root-Cause Debugging
    if secondary_skill:
        questions.append(
            f"Describe a severe production incident, memory leak, or latency spike involving {secondary_skill} or related infrastructure that you had to diagnose. What tools and step-by-step methodology did you use to isolate the root cause?"
        )
    else:
        questions.append(
            f"Describe the most challenging production bug, system crash, or data inconsistency you have resolved. What was your systematic process from diagnosis to permanent fix?"
        )

    # 3. System Design & Scalability Trade-offs
    if level in ("senior", "lead", "architect"):
        questions.append(
            f"If {company}'s active user traffic or data volume surged by 10x overnight, which component of your architecture would fail first, and how would you redesign it for fault tolerance and horizontal scale?"
        )
    elif level == "fresher":
        questions.append(
            f"When you are assigned an unfamiliar codebase or complex technical task as a junior {title}, what is your structured approach to reading documentation, writing automated tests, and delivering maintainable code?"
        )
    else:
        questions.append(
            f"How do you design modular APIs and service boundaries that balance rapid feature delivery with long-term security, backward compatibility, and maintainability?"
        )

    # 4. Behavioral & Cross-Functional Collaboration (STAR)
    questions.append(
        f"Tell me about a time when project requirements suddenly changed mid-sprint, or you had a technical disagreement with a teammate or product manager. How did you handle it and what was the outcome?"
    )

    # 5. Role & Company Strategic Alignment
    questions.append(
        f"Why are you specifically interested in {company}'s engineering culture, and how do you plan to make a measurable technical impact in the {title} position within your first 90 days?"
    )

    return questions


def _gemini_answer_feedback(question, answer, job, api_key):
    """Call Gemini to get an expert hiring manager evaluation."""
    skills = ", ".join(s.name for s in job.skills.all()[:5]) or "General Engineering"
    prompt = f"""You are a Senior Technical Hiring Manager at {job.company} evaluating a candidate's interview answer for the position of {job.title}.

Job Stack/Skills: {skills}
Interview Question: {question}
Candidate's Answer: {answer}

Provide an exhaustive, professional, constructive critique formatted EXACTLY with these 4 sections:

[EVALUATION SCORE & READINESS]: [X.X / 5.0 — Rating Label (e.g. Exceptional / Strong / Competent / Developing / Needs Revision)]
A 1-2 sentence executive summary of whether this answer meets hiring bar expectations at {job.company}.

[KEY STRENGTHS]:
- [Specific strength 1 based directly on their answer]
- [Specific strength 2, e.g. technical depth, clear ownership, relevant tools]

[AREAS TO IMPROVE]:
- [Specific gap 1: e.g. missing quantifiable metrics (latency, %, scale), missing STAR framework structure, vague technical details, or missing trade-offs]
- [Specific gap 2: how an interviewer will perceive this omission and how to fix it]

[RECOMMENDED MODEL ANSWER]:
[A concrete, realistic 3-5 sentence example demonstrating how a top-tier candidate answers this question using the STAR method (Situation, Task, Action, Result) with metrics and technical specifics.]"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=12) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        return data["candidates"][0]["content"]["parts"][0]["text"].strip()


def _rule_based_answer_feedback(question, answer, job):
    """
    Comprehensive, multi-dimensional offline interview evaluation engine.
    Examines answer length, STAR alignment, technical depth, quantifiable impact,
    tonal confidence, and architectural trade-offs so feedback never lacks depth
    for ANY kind of answer.
    """
    raw_text = answer.strip()
    words = re.findall(r"\b[\w'-]+\b", raw_text)
    word_count = len(words)
    lower_text = raw_text.lower()

    # 1. Detect Trivial or Empty Answers
    trivial_phrases = {
        "yes", "no", "i know it", "i did it", "not much", "idk", "good", "used it",
        "i have experience", "fine", "nothing", "i can do it", "i know", "i dont know",
        "i don't know", "na", "n/a", "ok", "okay"
    }
    is_trivial = word_count < 15 or lower_text in trivial_phrases

    # 2. Detect Textbook / Definition-only Answers (lack personal experience)
    has_first_person = bool(re.search(r"\b(i|my|we|our|me)\b", lower_text))
    is_definition = bool(re.search(r"\b(is a|is an|stands for|is defined as|refers to|is used to|is an open[- ]source)\b", lower_text)) and not has_first_person

    # 3. Detect Hesitant or Weak Phrasing
    hesitant_matches = re.findall(r"\b(i think maybe|i guess|not sure|probably|kind of|sort of|i believe maybe|someone told me)\b", lower_text)

    # 4. STAR Component Analysis
    has_situation = bool(re.search(r"\b(when|while|during|project|system|client|production|company|app|database|api|user|traffic|incident|outage|legacy|requirement)\b", lower_text))
    has_action = bool(re.search(r"\b(built|implemented|designed|architected|refactored|migrated|debugged|optimized|configured|wrote|tested|deployed|profiled|created|isolated|analyzed|automated|introduced)\b", lower_text))
    has_result = bool(re.search(r"\b(reduced|increased|improved|saved|boosted|resolved|prevented|scaled|delivered|resulting in|outcome|achieved|allowed us|decreased|eliminated)\b", lower_text))
    has_metrics = bool(re.search(r"(\d+(\.\d+)?\s*(%|percent|ms|s|sec|seconds|min|minutes|hours|days|x|k|m|million|users|req|rps|qps|mb|gb|tb|lpa))|\b\d+\b", lower_text))
    has_tradeoffs = bool(re.search(r"\b(because|trade-off|tradeoff|tradeoffs|instead of|alternative|chose|opted to|compared to|bottleneck|overhead|drawback|pros and cons)\b", lower_text))

    # 5. Check technical skill mentions
    job_skills = [s.name for s in job.skills.all()]
    matched_skills = [s for s in job_skills if s.lower() in lower_text]

    # Calculate Score
    if is_trivial:
        score = 1.0
        score_label = "1.0 / 5.0 - Critical: Far Too Brief"
    elif is_definition:
        score = 2.0
        score_label = "2.0 / 5.0 - Theoretical: Missing Firsthand Experience"
    else:
        score = 2.5
        if word_count >= 50:
            score += 0.5
        if 80 <= word_count <= 220:
            score += 0.5
        if has_action:
            score += 0.5
        if has_result:
            score += 0.5
        if has_metrics:
            score += 0.5
        if has_tradeoffs:
            score += 0.3
        if matched_skills:
            score += 0.2
        if hesitant_matches:
            score -= 0.5

        score = max(1.0, min(5.0, round(score, 1)))

        if score >= 4.5:
            score_label = f"{score} / 5.0 - Exceptional: Interview Ready"
        elif score >= 3.8:
            score_label = f"{score} / 5.0 - Strong: Solid Technical Narrative"
        elif score >= 3.0:
            score_label = f"{score} / 5.0 - Competent: Needs Quantifiable Impact"
        elif score >= 2.0:
            score_label = f"{score} / 5.0 - Developing: Lacks Depth & Context"
        else:
            score_label = f"{score} / 5.0 - Needs Significant Revision"

    # Assemble Strengths
    strengths = []
    if is_trivial:
        strengths.append("Submitted a response, but it lacks sufficient technical substance for hiring assessment.")
    elif is_definition:
        strengths.append("Demonstrated conceptual familiarity with the terminology and high-level concepts.")
    else:
        if has_action:
            strengths.append("Clear ownership of execution: Used active engineering verbs demonstrating direct hands-on responsibility.")
        if matched_skills:
            strengths.append(f"Direct technical relevance: Explicitly referenced relevant stack components ({', '.join(matched_skills[:3])}).")
        if has_metrics:
            strengths.append("Data-driven framing: Included quantitative metrics and scale markers to validate the impact.")
        if has_situation and has_result:
            strengths.append("Structured narrative: Established a clear problem statement and brought it through to a concrete outcome.")
        if 70 <= word_count <= 200:
            strengths.append(f"Ideal response length ({word_count} words): Long enough for depth, concise enough to keep the interviewer engaged.")

    if not strengths:
        strengths.append("Communicated clearly in straightforward language.")

    # Assemble Gaps & Areas to Improve
    gaps = []
    if is_trivial:
        gaps.append("Answer is too brief to evaluate your technical competency. In tech interviews, one-line answers signal disinterest or lack of hands-on experience.")
        gaps.append("Missing the STAR framework: Set the context (Situation), state your role (Task), describe your code/architecture (Action), and quantify what changed (Result).")
    elif is_definition:
        gaps.append("Interviewers test for battle-tested problem solving, not dictionary definitions. Avoid explaining what the tool is; explain how YOU applied it.")
        gaps.append("Add a personal project story: 'In my project at [Company/School], I used this tool to build [Feature] and solve [Bottleneck]...'")
    else:
        if not has_metrics:
            gaps.append("Missing Measurable Results: Add concrete numbers (e.g., 'reduced query time by 40%', 'processed 50k events/day', 'improved Lighthouse score from 65 to 94').")
        if not has_tradeoffs:
            gaps.append("Missing Technical Trade-offs: Senior interviewers want to know WHY you chose this approach over alternatives (e.g. Redis vs database caching, or monolith vs microservices).")
        if hesitant_matches:
            gaps.append(f"Hesitant Phrasing: Words like '{', '.join(hesitant_matches[:2])}' erode interviewer confidence. Speak with conviction: 'Based on our benchmarks, we decided to...'")
        if word_count < 50:
            gaps.append(f"Answer is concise ({word_count} words). Aim for 80-150 words to provide complete context without trailing off.")
        elif word_count > 250:
            gaps.append(f"Answer is somewhat verbose ({word_count} words). In live interviews, aim for 1.5 to 2 minutes of spoken time (around 120-180 words) to avoid losing the interviewer's attention.")
        if not has_action:
            gaps.append("Clarify your specific personal contribution: State what YOU built or fixed rather than vague team efforts ('we did').")

    if not gaps:
        gaps.append("Prepare for advanced follow-ups: The interviewer will likely drill into disaster recovery, concurrency bottlenecks, or how your solution would scale to 10x traffic.")

    # Generate Tailored Model Answer
    title = job.title or "Software Developer"
    company = job.company or "the engineering team"
    primary_tool = job_skills[0] if job_skills else "the technical stack"

    q_lower = question.lower()
    if any(k in q_lower for k in ["concurrency", "optimize", "query", "state", "architecture", "scale"]):
        model_answer = (
            f"\"In my recent project, our application faced severe latency spikes during peak user hours. "
            f"As lead engineer on the feature, I profiled the system and identified unindexed database queries and repetitive network round-trips. "
            f"I introduced targeted indexing combined with an asynchronous worker pipeline in {primary_tool}, "
            f"which reduced p95 latency from 850ms to 95ms and supported a 4x increase in concurrent traffic without adding extra server capacity.\""
        )
    elif any(k in q_lower for k in ["incident", "leak", "bug", "crash", "diagnose"]):
        model_answer = (
            f"\"During a production release, our service experienced unexpected CPU spikes leading to intermittent timeouts. "
            f"I checked APM telemetry and server logs to isolate a memory leak caused by unclosed connection pools in our background worker. "
            f"I refactored the connection lifecycle using context-managed pools with timeout safeguards and added automated regression tests. "
            f"This restored 99.99% uptime and completely eliminated connection pool exhaustion.\""
        )
    elif any(k in q_lower for k in ["why are you", "interested in", "90 days", "impact"]):
        model_answer = (
            f"\"I have been closely following {company}'s technical trajectory and high engineering standards. "
            f"In my first 30 days, I plan to master your deployment workflows, codebase architecture, and internal standards. "
            f"By day 60, I expect to take full ownership of feature releases in {primary_tool}, and by day 90, "
            f"contribute directly to performance optimizations, code review velocity, and mentoring team members.\""
        )
    else:
        model_answer = (
            f"\"When our team faced shifting project deadlines, I led a rapid technical triage with stakeholders to protect our core deliverables. "
            f"I negotiated scoping the minimum viable schema for sprint delivery and deferred non-critical reporting jobs. "
            f"By establishing clear API contracts and pairing with our QA engineer, we shipped the release on time with 100% test pass rate and zero critical rollbacks.\""
        )

    # Format into structured feedback text
    strengths_text = "\n".join(f"- {s}" for s in strengths)
    gaps_text = "\n".join(f"- {g}" for g in gaps)

    return (
        f"[EVALUATION SCORE & READINESS]: {score_label}\n\n"
        f"[KEY STRENGTHS]:\n{strengths_text}\n\n"
        f"[AREAS TO IMPROVE]:\n{gaps_text}\n\n"
        f"[RECOMMENDED MODEL ANSWER]:\n{model_answer}"
    )


def answer_feedback(question, answer, job):
    """
    Evaluates interview answers with zero gaps:
    Uses Gemini AI if configured, or the comprehensive offline heuristic engine.
    Always delivers Score, Strengths, Actionable Gaps, and a Concrete Model Answer.
    """
    api_key = getattr(settings, "GEMINI_API_KEY", "")
    if api_key:
        try:
            gemini_res = _gemini_answer_feedback(question, answer, job, api_key)
            if gemini_res and len(gemini_res.strip()) > 50:
                return gemini_res
        except Exception:
            pass

    return _rule_based_answer_feedback(question, answer, job)
