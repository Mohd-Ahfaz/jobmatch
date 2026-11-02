from datetime import date, timedelta

from django.core.management.base import BaseCommand

from accounts.models import Question, Skill
from accounts.sample_data import JOBS, QUESTIONS, SKILLS, SUSPICIOUS_JOBS
from jobs.models import Job


class Command(BaseCommand):
    help = "Adds sample skills, quiz questions and jobs"

    def handle(self, *args, **options):
        # Create ALL skills first (including those without quiz questions)
        skills = {}
        for name in SKILLS:
            obj, created = Skill.objects.get_or_create(name=name)
            skills[name] = obj
            if created:
                self.stdout.write(f"  Created skill: {name}")

        self.stdout.write(self.style.SUCCESS(f"Skills: {len(skills)} total in database."))

        # Create quiz questions for skills that have them
        q_count = 0
        for skill_name, questions in QUESTIONS.items():
            if skill_name not in skills:
                continue
            for text, options_list, right in questions:
                _, created = Question.objects.get_or_create(
                    skill=skills[skill_name],
                    text=text,
                    defaults={
                        "option_a": options_list[0],
                        "option_b": options_list[1],
                        "option_c": options_list[2],
                        "option_d": options_list[3],
                        "correct": "abcd"[right],
                    },
                )
                if created:
                    q_count += 1

        self.stdout.write(self.style.SUCCESS(f"Quiz questions: {q_count} new questions created."))

        # Create regular real jobs
        job_count = 0
        for number, row in enumerate(JOBS):
            title, company, location, remote, level, low, high, skill_names, apply_link, contact_email, description = row
            job, created = Job.objects.update_or_create(
                title=title,
                company=company,
                defaults={
                    "location": location,
                    "is_remote": remote,
                    "level": level,
                    "min_salary": low,
                    "max_salary": high,
                    "description": description,
                    "apply_link": apply_link,
                    "contact_email": contact_email,
                    "posted_on": date.today() - timedelta(days=number * 2),
                    "is_real": True,
                    "source": "Verified Career Portal",
                },
            )
            job.skills.set([skills[name] for name in skill_names if name in skills])
            if created:
                job_count += 1

        self.stdout.write(self.style.SUCCESS(f"Real Jobs: {len(JOBS)} loaded ({job_count} newly created)."))

        # Create suspicious/scam jobs
        scam_count = 0
        for number, data in enumerate(SUSPICIOUS_JOBS):
            fields = {key: value for key, value in data.items() if key != "skills"}
            job, created = Job.objects.get_or_create(
                title=data["title"],
                company=data["company"],
                defaults={
                    **fields,
                    "posted_on": date.today() - timedelta(days=number),
                    "is_real": False,
                    "source": "Scam Shield Demo",
                },
            )
            if created:
                job.skills.set([skills[name] for name in data["skills"] if name in skills])
                scam_count += 1

        self.stdout.write(self.style.SUCCESS(f"Scam jobs: {scam_count} created."))
        self.stdout.write(self.style.SUCCESS("[OK] Sample data loaded successfully."))
