# JobMatch - Job Market Skill Analyzer

Django + MySQL + Bootstrap project. It matches your skills with job listings, warns about scam jobs,
helps you prepare applications, and tracks every application on a board.

## Setup

1. Install Python 3.10+ and MySQL, then create the database:

   ```sql
   CREATE DATABASE jobmatch CHARACTER SET utf8mb4;
   ```

2. Open `jobmatch/settings.py` and set your MySQL `USER` and `PASSWORD` in `DATABASES`.

3. Install the packages and create the tables:

   ```
   python -m venv venv
   venv\Scripts\activate          (Windows)   |   source venv/bin/activate   (Mac/Linux)
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py load_sample_data
   python manage.py createsuperuser
   python manage.py runserver
   ```

4. Open http://127.0.0.1:8000/

`load_sample_data` adds 17 skills, 30 quiz questions and 20 jobs (3 of them are fake-looking on purpose,
so you can see the Scam Shield work). Add more jobs any time from http://127.0.0.1:8000/admin/

If `mysqlclient` fails to install, run `pip install pymysql` and add these two lines at the top of
`jobmatch/__init__.py`:

```python
import pymysql
pymysql.install_as_MySQLdb()
```

## Project layout

| Folder     | What it does                                                          |
|------------|-----------------------------------------------------------------------|
| accounts   | Sign up, login, password reset, dashboard, profile + resume, skill quiz |
| jobs       | Job feed with filters, job detail, match %, scam shield, salary, chance score |
| tracker    | Kanban board, apply links, resume/cover letter, ATS check, interview prep |
| growth     | Skill gap, what-if simulator, rejection fix, insights                 |
| templates  | All HTML pages (Bootstrap 5)                                          |
| static     | `css/style.css` (white theme with violet and pink) and `js/main.js`   |

## Notes

- Matching, scam checks, ATS score and interview feedback use simple rules in `jobs/utils.py` and
  `tracker/utils.py`, so the logic is easy to read and change.
- Password reset emails are printed in the terminal (change `EMAIL_BACKEND` in settings to send real mail).
- Skill-based Applications: You can apply for any job directly using your matched skills. The platform compiles your matching skills, tailored cover letter, and resume into an application package, sends it, and sets a follow-up reminder on your tracker.
