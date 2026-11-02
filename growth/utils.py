from urllib.parse import quote

COURSES = {
    # Original
    "Python": ("Python for Everybody", "https://www.py4e.com/"),
    "SQL": ("SQLBolt interactive lessons", "https://sqlbolt.com/"),
    "JavaScript": ("The Modern JavaScript Tutorial", "https://javascript.info/"),
    "HTML": ("MDN Learn web development", "https://developer.mozilla.org/en-US/docs/Learn_web_development"),
    "CSS": ("MDN Learn web development", "https://developer.mozilla.org/en-US/docs/Learn_web_development"),
    "Django": ("Official Django tutorial", "https://docs.djangoproject.com/en/stable/intro/tutorial01/"),
    "Machine Learning": ("Kaggle: Intro to Machine Learning", "https://www.kaggle.com/learn/intro-to-machine-learning"),
    "Git": ("Learn Git Branching", "https://learngitbranching.js.org/"),
    "Docker": ("Docker: Get started", "https://docs.docker.com/get-started/"),
    "Pandas": ("Kaggle: Pandas", "https://www.kaggle.com/learn/pandas"),
    "Java": ("Dev.java: Learn", "https://dev.java/learn/"),
    "React": ("React: Learn", "https://react.dev/learn"),
    "Statistics": ("Khan Academy: Statistics", "https://www.khanacademy.org/math/statistics-probability"),
    "Deep Learning": ("Kaggle: Intro to Deep Learning", "https://www.kaggle.com/learn/intro-to-deep-learning"),
    "AWS": ("AWS Skill Builder", "https://explore.skillbuilder.aws/learn"),
    "Flask": ("Flask quickstart", "https://flask.palletsprojects.com/en/stable/quickstart/"),
    "Power BI": ("Microsoft Learn: Power BI", "https://learn.microsoft.com/en-us/training/powerplatform/power-bi"),
    # Web & Frontend
    "TypeScript": ("TypeScript Handbook", "https://www.typescriptlang.org/docs/handbook/intro.html"),
    "Angular": ("Angular: Getting Started", "https://angular.dev/tutorials/learn-angular"),
    "Vue.js": ("Vue.js Official Guide", "https://vuejs.org/guide/introduction.html"),
    "Bootstrap": ("Bootstrap: Getting Started", "https://getbootstrap.com/docs/5.3/getting-started/introduction/"),
    "Tailwind CSS": ("Tailwind CSS Docs", "https://tailwindcss.com/docs/installation"),
    "jQuery": ("jQuery Learning Center", "https://learn.jquery.com/"),
    "Next.js": ("Next.js Learn", "https://nextjs.org/learn"),
    "GraphQL": ("How to GraphQL", "https://www.howtographql.com/"),
    "REST API": ("REST API Tutorial", "https://restfulapi.net/"),
    # Backend & Databases
    "Node.js": ("Node.js Official Docs", "https://nodejs.org/en/learn/getting-started/introduction-to-nodejs"),
    "Express.js": ("Express.js Guide", "https://expressjs.com/en/guide/routing.html"),
    "Spring Boot": ("Spring Guides", "https://spring.io/guides"),
    "FastAPI": ("FastAPI Tutorial", "https://fastapi.tiangolo.com/tutorial/"),
    "Laravel": ("Laravel Docs", "https://laravel.com/docs/"),
    "MongoDB": ("MongoDB University", "https://learn.mongodb.com/"),
    "PostgreSQL": ("PostgreSQL Tutorial", "https://www.postgresqltutorial.com/"),
    "MySQL": ("MySQL Tutorial", "https://dev.mysql.com/doc/refman/8.0/en/tutorial.html"),
    "Redis": ("Redis University", "https://university.redis.com/"),
    "Elasticsearch": ("Elastic Learn", "https://www.elastic.co/training/"),
    # Data & AI
    "NumPy": ("NumPy Quickstart", "https://numpy.org/doc/stable/user/quickstart.html"),
    "Matplotlib": ("Matplotlib Tutorials", "https://matplotlib.org/stable/tutorials/index.html"),
    "Seaborn": ("Seaborn Tutorial", "https://seaborn.pydata.org/tutorial.html"),
    "Scikit-learn": ("Scikit-learn Tutorials", "https://scikit-learn.org/stable/tutorial/index.html"),
    "TensorFlow": ("TensorFlow Tutorials", "https://www.tensorflow.org/tutorials"),
    "PyTorch": ("PyTorch Tutorials", "https://pytorch.org/tutorials/"),
    "OpenCV": ("OpenCV Python Tutorials", "https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html"),
    "NLP": ("Kaggle: NLP", "https://www.kaggle.com/learn/natural-language-processing"),
    "Tableau": ("Tableau Training", "https://www.tableau.com/learn/training"),
    "Excel": ("Microsoft Excel Training", "https://support.microsoft.com/en-us/office/excel-video-training-9bc05390-e94c-46af-a5b3-d7c22f6990bb"),
    # DevOps & Cloud
    "Kubernetes": ("Kubernetes Docs", "https://kubernetes.io/docs/tutorials/"),
    "Linux": ("Linux Journey", "https://linuxjourney.com/"),
    "Bash": ("Bash Scripting Tutorial", "https://www.shellscript.sh/"),
    "CI/CD": ("GitHub Actions Docs", "https://docs.github.com/en/actions"),
    "Terraform": ("HashiCorp Learn Terraform", "https://developer.hashicorp.com/terraform/tutorials"),
    "Azure": ("Microsoft Learn: Azure", "https://learn.microsoft.com/en-us/training/azure/"),
    "Google Cloud": ("Google Cloud Skills Boost", "https://www.cloudskillsboost.google/"),
    "Jenkins": ("Jenkins Documentation", "https://www.jenkins.io/doc/tutorials/"),
    "Nginx": ("Nginx Beginner's Guide", "https://nginx.org/en/docs/beginners_guide.html"),
    # Programming Languages
    "C": ("C Programming Tutorial", "https://www.learn-c.org/"),
    "C++": ("LearnCpp.com", "https://www.learncpp.com/"),
    "C#": ("Microsoft Learn: C#", "https://learn.microsoft.com/en-us/dotnet/csharp/tour-of-csharp/"),
    ".NET": ("Microsoft Learn: .NET", "https://dotnet.microsoft.com/en-us/learn"),
    "PHP": ("PHP Manual", "https://www.php.net/manual/en/getting-started.php"),
    "Kotlin": ("Kotlin Docs", "https://kotlinlang.org/docs/getting-started.html"),
    "Swift": ("Swift.org: Getting Started", "https://www.swift.org/getting-started/"),
    "R": ("R for Data Science", "https://r4ds.hadley.nz/"),
    "Go": ("Go Tour", "https://go.dev/tour/welcome/1"),
    # Tools & Other
    "Figma": ("Figma Basics", "https://help.figma.com/hc/en-us/articles/360038006233"),
    "Jira": ("Atlassian Jira Basics", "https://www.atlassian.com/software/jira/guides"),
    "Postman": ("Postman Learning Center", "https://learning.postman.com/docs/getting-started/introduction/"),
    "Firebase": ("Firebase Docs", "https://firebase.google.com/docs"),
    "Selenium": ("Selenium Docs", "https://www.selenium.dev/documentation/"),
    "Unit Testing": ("pytest Docs", "https://docs.pytest.org/en/stable/getting-started.html"),
    "Agile": ("Atlassian Agile Coach", "https://www.atlassian.com/agile"),
    "MATLAB": ("MathWorks MATLAB Tutorials", "https://www.mathworks.com/support/learn-with-matlab-tutorials.html"),
    "Hadoop": ("Hadoop Tutorial", "https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/SingleCluster.html"),
    "Spark": ("Apache Spark Quickstart", "https://spark.apache.org/docs/latest/quick-start.html"),
}

REJECTION_TIPS = [
    (["experience", "years", "senior"], "Add projects, internships or open source work to show practical experience."),
    (["skills", "qualification", "technical", "requirements"], "Match your resume to the job's required skills and take the skill quizzes to get verified."),
    (["other candidate", "better fit", "moved forward", "another candidate"], "Apply earlier and follow up within a week to stay on the recruiter's radar."),
    (["interview", "communication", "answers"], "Practice answers in Interview Prep and keep each one specific, with a result."),
    (["salary", "budget", "compensation"], "Check your expected salary against similar jobs in the feed."),
]


def course_for(skill):
    if skill in COURSES:
        return COURSES[skill]
    return (f"Search free {skill} courses", "https://www.youtube.com/results?search_query=" + quote(f"learn {skill}"))
