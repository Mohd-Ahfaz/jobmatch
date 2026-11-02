SKILLS = [
    # Original 17
    "Python", "SQL", "JavaScript", "HTML", "CSS", "Django", "Machine Learning", "Git",
    "Docker", "Pandas", "Java", "React", "Statistics", "Deep Learning", "AWS", "Flask", "Power BI",

    # Web & Frontend
    "TypeScript", "Angular", "Vue.js", "Bootstrap", "Tailwind CSS", "jQuery",
    "Next.js", "GraphQL", "REST API",

    # Backend & Databases
    "Node.js", "Express.js", "Spring Boot", "FastAPI", "Laravel",
    "MongoDB", "PostgreSQL", "MySQL", "Redis", "Elasticsearch",

    # Data & AI
    "NumPy", "Matplotlib", "Seaborn", "Scikit-learn", "TensorFlow",
    "PyTorch", "OpenCV", "NLP", "Tableau", "Excel",

    # DevOps & Cloud
    "Kubernetes", "Linux", "Bash", "CI/CD", "Terraform",
    "Azure", "Google Cloud", "Jenkins", "Nginx",

    # Programming Languages
    "C", "C++", "C#", ".NET", "PHP", "Kotlin", "Swift", "R", "Go",

    # Tools & Other
    "Figma", "Jira", "Postman", "Firebase", "Selenium",
    "Unit Testing", "Agile", "MATLAB", "Hadoop", "Spark",
]

# skill: [(question, [4 options], index of the right option)]
QUESTIONS = {
    "Python": [
        ("What does len([1, 2, 3]) return?", ["2", "3", "4", "Error"], 1),
        ("Which keyword is used to define a function?", ["func", "define", "def", "function"], 2),
        ("What is the type of {}?", ["list", "dict", "set", "tuple"], 1),
    ],
    "SQL": [
        ("Which command gets data from a table?", ["GET", "SELECT", "FETCH", "OPEN"], 1),
        ("Which clause filters rows after grouping?", ["WHERE", "ORDER BY", "HAVING", "LIMIT"], 2),
        ("Which join returns only matching rows from both tables?", ["INNER JOIN", "LEFT JOIN", "FULL JOIN", "CROSS JOIN"], 0),
    ],
    "JavaScript": [
        ("Which keyword declares a variable that cannot be reassigned?", ["var", "let", "const", "static"], 2),
        ("What does === check?", ["Value only", "Type only", "Value and type", "Neither"], 2),
        ("Which method adds an item to the end of an array?", ["push()", "pop()", "shift()", "add()"], 0),
    ],
    "HTML": [
        ("Which tag creates a link?", ["<link>", "<a>", "<href>", "<url>"], 1),
        ("Which tag makes the largest heading?", ["<h6>", "<head>", "<h1>", "<title>"], 2),
        ("Which attribute gives alternative text for an image?", ["title", "alt", "src", "name"], 1),
    ],
    "CSS": [
        ("Which property changes text color?", ["font-color", "text-color", "color", "background"], 2),
        ("Which display value builds flexible row layouts?", ["flex", "block", "inline", "none"], 0),
        ("What does margin control?", ["Space inside an element", "Space outside an element", "Text size", "Border color"], 1),
    ],
    "Django": [
        ("Which file holds the URL routes of an app?", ["urls.py", "models.py", "views.py", "admin.py"], 0),
        ("Which commands create database tables from models?", ["runserver", "makemigrations and migrate", "startapp", "collectstatic"], 1),
        ("What does the Django ORM let you do?", ["Style pages", "Query the database with Python", "Send emails only", "Compile JavaScript"], 1),
    ],
    "Machine Learning": [
        ("Which type of learning uses labelled data?", ["Supervised", "Unsupervised", "Reinforcement", "None of these"], 0),
        ("What is overfitting?", ["The model is too simple", "The model fits training data too closely and fails on new data", "The model trains too fast", "The model has no data"], 1),
        ("Which metric is common for classification?", ["Accuracy", "Mean squared error", "R-squared", "Mean absolute error"], 0),
    ],
    "Git": [
        ("Which command saves changes to the local history?", ["git push", "git commit", "git pull", "git clone"], 1),
        ("Which command downloads a remote repository?", ["git clone", "git init", "git add", "git merge"], 0),
        ("Which command creates a new branch?", ["git branch name", "git new name", "git fork name", "git split name"], 0),
    ],
    "Docker": [
        ("What is a Docker image?", ["A running container", "A read-only template used to create containers", "A virtual machine", "A database"], 1),
        ("Which file describes how to build an image?", ["Dockerfile", "docker.json", "build.txt", "compose.py"], 0),
        ("Which command lists running containers?", ["docker images", "docker ps", "docker run", "docker list"], 1),
    ],
    "Pandas": [
        ("Which function reads a CSV file?", ["pd.read_csv()", "pd.open_csv()", "pd.load()", "pd.csv()"], 0),
        ("What does df.head() show?", ["The last 5 rows", "The first 5 rows", "The column names", "The row count"], 1),
        ("Which method removes missing values?", ["df.dropna()", "df.remove()", "df.clean()", "df.nonull()"], 0),
    ],
    "TypeScript": [
        ("What does TypeScript add to JavaScript?", ["Faster runtime", "Static types", "A new runtime", "HTML support"], 1),
        ("Which keyword defines a TypeScript interface?", ["type", "interface", "class", "struct"], 1),
        ("What does the 'any' type do in TypeScript?", ["Throws an error", "Disables type checking for that value", "Only allows strings", "Only allows numbers"], 1),
    ],
    "React": [
        ("What is JSX?", ["A database query language", "A syntax extension that lets you write HTML in JavaScript", "A CSS preprocessor", "A testing framework"], 1),
        ("Which hook manages state in a function component?", ["useEffect", "useState", "useRef", "useContext"], 1),
        ("What does the virtual DOM do in React?", ["Stores data", "Speeds up updates by comparing changes before applying them", "Handles routing", "Manages API calls"], 1),
    ],
    "Node.js": [
        ("What is Node.js?", ["A browser", "A JavaScript runtime built on Chrome's V8 engine", "A database", "A CSS framework"], 1),
        ("Which module handles file operations in Node.js?", ["http", "fs", "path", "os"], 1),
        ("What does npm stand for?", ["Node Package Manager", "New Project Module", "Node Program Manager", "None of these"], 0),
    ],
    "MongoDB": [
        ("What type of database is MongoDB?", ["Relational", "Document-oriented NoSQL", "Graph", "Columnar"], 1),
        ("Which format does MongoDB store data in?", ["XML", "JSON-like BSON documents", "CSV", "Plain text"], 1),
        ("Which command inserts a document?", ["db.collection.add()", "db.collection.insert()", "db.collection.insertOne()", "db.collection.put()"], 2),
    ],
    "NumPy": [
        ("What is NumPy primarily used for?", ["Web development", "Numerical computing with arrays", "Database management", "Game development"], 1),
        ("Which function creates an array of zeros?", ["np.zeros()", "np.empty()", "np.blank()", "np.null()"], 0),
        ("What does np.reshape() do?", ["Deletes an array", "Changes the shape of an array without changing data", "Sorts the array", "Reverses the array"], 1),
    ],
    "Linux": [
        ("Which command lists files in a directory?", ["dir", "ls", "list", "show"], 1),
        ("Which command changes file permissions?", ["chown", "chmod", "chperm", "access"], 1),
        ("Which command shows running processes?", ["ps", "run", "proc", "task"], 0),
    ],
    "Kubernetes": [
        ("What is a Pod in Kubernetes?", ["A physical server", "The smallest deployable unit containing one or more containers", "A network policy", "A storage class"], 1),
        ("Which command applies a configuration file?", ["kubectl run", "kubectl apply -f", "kubectl create", "kubectl start"], 1),
        ("What does a Service do in Kubernetes?", ["Builds images", "Exposes pods to network traffic", "Scales replicas", "Stores secrets"], 1),
    ],
    "C++": [
        ("Which keyword is used for inheritance in C++?", ["extends", "inherits", ":", "->"], 2),
        ("What is a pointer in C++?", ["A type of loop", "A variable that stores a memory address", "A string method", "An array type"], 1),
        ("Which operator is used to access a member via a pointer?", [".", "::", "->", "&"], 2),
    ],
    "TensorFlow": [
        ("What is TensorFlow primarily used for?", ["Web scraping", "Building and training machine learning models", "Database management", "UI design"], 1),
        ("What is a tensor?", ["A type of loop", "A multi-dimensional array of numbers", "A Python dictionary", "A network request"], 1),
        ("Which API in TensorFlow is used for building models layer by layer?", ["tf.data", "tf.keras", "tf.nn", "tf.function"], 1),
    ],
    "PostgreSQL": [
        ("Which data type stores variable-length text in PostgreSQL?", ["TEXT", "CHAR", "BLOB", "NVARCHAR"], 0),
        ("Which command creates a new database?", ["MAKE DATABASE", "CREATE DATABASE", "NEW DATABASE", "INIT DATABASE"], 1),
        ("What is a schema in PostgreSQL?", ["A type of index", "A namespace that organises database objects", "A stored procedure", "A trigger"], 1),
    ],
    ".NET": [
        ("Which language is the primary language used to build modern .NET applications?", ["C#", "Java", "Swift", "PHP"], 0),
        ("What is the runtime environment that executes .NET programs and provides memory management?", ["JVM", "CLR (Common Language Runtime)", "V8", "Node.js"], 1),
        ("Which framework is used to build modern cross-platform web APIs in .NET?", ["ASP.NET Core", "Django", "Spring Boot", "Laravel"], 0),
    ],
    "Agile": [
        ("In Scrum, how long is a typical Sprint iteration?", ["1 to 4 weeks", "6 months", "1 day", "1 year"], 0),
        ("What is the primary purpose of the daily standup meeting in Agile?", ["Status reporting to management", "Synchronizing team progress and surfacing blockers", "Assigning blame for bugs", "Writing sprint documentation"], 1),
        ("What artifact contains the prioritized list of all desired product features?", ["Sprint Backlog", "Product Backlog", "Burndown Chart", "Retrospective Log"], 1),
    ],
    "Angular": [
        ("Which programming language is primarily used with modern Angular?", ["TypeScript", "Python", "Ruby", "PHP"], 0),
        ("Which decorator is used to define a component in Angular?", ["@Injectable()", "@Component()", "@Directive()", "@NgModule()"], 1),
        ("What is the official command-line tool used to create, build, and test Angular projects?", ["npm", "Angular CLI (ng)", "Webpack", "Vite"], 1),
    ],
    "AWS": [
        ("Which AWS service provides resizable virtual compute servers in the cloud?", ["Amazon S3", "Amazon EC2", "Amazon RDS", "AWS Lambda"], 1),
        ("Which AWS service is an object storage service offering high scalability and availability?", ["Amazon S3", "Amazon EBS", "Amazon EFS", "Amazon DynamoDB"], 0),
        ("Which AWS service allows running serverless code triggered by events?", ["Amazon EC2", "AWS Lambda", "Amazon ECS", "AWS CloudFormation"], 1),
    ],
    "Azure": [
        ("What is Microsoft's primary service for running scalable virtual machines in Azure?", ["Azure Virtual Machines (VM)", "Azure Blob Storage", "Azure SQL", "Azure Functions"], 0),
        ("Which Azure service provides scalable, serverless event-driven computing?", ["Azure Virtual Network", "Azure Functions", "Azure DevOps", "Azure Active Directory"], 1),
        ("Which Azure service is optimized for storing massive amounts of unstructured object data?", ["Azure Cosmos DB", "Azure Blob Storage", "Azure Files", "Azure Table Storage"], 1),
    ],
    "Bash": [
        ("Which command displays the current working directory in Bash?", ["ls", "pwd", "cd", "dir"], 1),
        ("Which line (shebang) specifies the Bash interpreter at the top of a script?", ["#!/bin/bash", "<!-- bash -->", "// bin/bash", "%%bash"], 0),
        ("How do you access the value of a variable named PORT in Bash?", ["$PORT", "%PORT%", "&PORT", "PORT.value"], 0),
    ],
    "Bootstrap": [
        ("How many columns are there in the default Bootstrap grid system?", ["10", "12", "16", "24"], 1),
        ("Which class provides a responsive, fixed-width or full-width container in Bootstrap?", [".container", ".box", ".wrapper", ".grid-row"], 0),
        ("Which Bootstrap class is used to style a primary action button?", [".btn .btn-primary", ".button-main", ".btn-submit", ".btn-blue"], 0),
    ],
    "C": [
        ("Which function dynamically allocates memory on the heap in C?", ["malloc()", "alloc()", "new", "create()"], 0),
        ("Which operator is used to obtain the memory address of a variable in C?", ["*", "&", "#", "->"], 1),
        ("What character marks the end of a string in C?", ["\\0 (null terminator)", "\\n", "\\t", "EOF"], 0),
    ],
    "C#": [
        ("Which keyword is used to create a new instance of an object in C#?", ["new", "create", "init", "make"], 0),
        ("Which feature in C# enables querying collections and databases using a readable syntax?", ["LINQ", "JDBC", "Pointers", "Streams"], 0),
        ("Which access modifier in C# makes a member accessible only within its own class?", ["public", "protected", "private", "internal"], 2),
    ],
    "CI/CD": [
        ("What does CI stand for in modern DevOps?", ["Continuous Integration", "Continuous Innovation", "Complete Installation", "Central Infrastructure"], 0),
        ("What is the primary goal of Continuous Delivery (CD)?", ["Automating code reviews", "Ensuring software can be reliably released to production at any time", "Replacing manual QA testers", "Eliminating branches"], 1),
        ("Which popular CI/CD tool uses GitHub repositories with workflows in .github/workflows?", ["GitHub Actions", "Travis CI", "Puppet", "Nagios"], 0),
    ],
    "Deep Learning": [
        ("Which type of neural network is typically best suited for image classification tasks?", ["RNN (Recurrent Neural Network)", "CNN (Convolutional Neural Network)", "Linear Regression", "K-Means"], 1),
        ("What problem occurs when gradients shrink exponentially during backpropagation in deep networks?", ["Vanishing gradient problem", "Overfitting", "Gradient explosion", "Underfitting"], 0),
        ("Which activation function is most commonly used in hidden layers of modern deep networks?", ["Step function", "Sigmoid", "ReLU (Rectified Linear Unit)", "Linear"], 2),
    ],
    "Elasticsearch": [
        ("What underlying open-source search library powers Elasticsearch?", ["Apache Lucene", "SQLite", "PostgreSQL", "Apache Solr"], 0),
        ("What is the basic unit of data stored in Elasticsearch?", ["JSON Document", "Table row", "Column family", "Tuple"], 0),
        ("Which HTTP method is used in the Elasticsearch REST API to perform a search query?", ["GET", "PUT", "DELETE", "PATCH"], 0),
    ],
    "Excel": [
        ("Which symbol must all Excel formulas begin with?", ["=", "@", "#", "+"], 0),
        ("Which function looks up a value in a column and returns a matching value from another column?", ["VLOOKUP (or XLOOKUP)", "FIND()", "SEARCH()", "COUNTIF()"], 0),
        ("What feature in Excel is used to summarize, analyze, and present data interactively?", ["PivotTable", "Conditional Formatting", "Sparklines", "AutoSum"], 0),
    ],
    "Express.js": [
        ("Which Node.js method is used to register route middleware in Express?", ["app.use()", "app.route()", "app.middleware()", "app.plugin()"], 0),
        ("How do you access route parameters (e.g. /users/:id) in an Express handler?", ["req.params.id", "req.query.id", "req.body.id", "req.headers.id"], 0),
        ("What method sends a JSON response from an Express route handler?", ["res.json()", "res.sendJson()", "res.write()", "res.output()"], 0),
    ],
    "FastAPI": [
        ("Which Python library does FastAPI use for data validation and settings management?", ["Pydantic", "Marshmallow", "Django ORM", "Cerberus"], 0),
        ("What automatic documentation UI does FastAPI generate at /docs?", ["Swagger / OpenAPI UI", "Javadoc", "Sphinx", "Postman Collection"], 0),
        ("Which ASGI web server is most commonly used to run production FastAPI apps?", ["Uvicorn", "Gunicorn (standalone)", "Apache", "Nginx (native ASGI)"], 0),
    ],
    "Figma": [
        ("What feature in Figma allows designers to create reusable UI elements across designs?", ["Components", "Frames", "Artboards", "Layers"], 0),
        ("Which Figma layout feature automatically adapts spacing and padding as content changes?", ["Auto Layout", "Grid Ruler", "Smart Animate", "Vector Network"], 0),
        ("What is Figma's primary collaboration advantage over legacy desktop design tools?", ["Real-time browser-based collaboration", "Offline-only desktop files", "Raster painting engine", "Native 3D rendering"], 0),
    ],
    "Firebase": [
        ("Which Google cloud service provides a NoSQL document database with real-time listeners?", ["Cloud Firestore", "Cloud Spanner", "BigQuery", "Cloud SQL"], 0),
        ("Which Firebase feature lets developers easily authenticate users with Google, email, and social providers?", ["Firebase Authentication", "Firebase Remote Config", "Firebase Test Lab", "Firebase Crashlytics"], 0),
        ("What are Firebase Cloud Functions?", ["Serverless backend code triggered by Firebase events and HTTPS requests", "Static website hosting", "Database backup scripts", "Mobile push notifications"], 0),
    ],
    "Flask": [
        ("What decorator is used in Flask to bind a view function to a URL route?", ["@app.route()", "@app.url()", "@app.view()", "@app.endpoint()"], 0),
        ("Which template engine is bundled by default with Flask?", ["Jinja2", "Django Templates", "Mako", "Handlebars"], 0),
        ("How do you access URL query parameters (e.g. ?page=2) in Flask?", ["request.args.get('page')", "request.form['page']", "request.params['page']", "request.query['page']"], 0),
    ],
    "Go": [
        ("What keyword is used to launch a concurrent lightweight thread of execution in Go?", ["go", "thread", "async", "spawn"], 0),
        ("How are typed communication and synchronization achieved between goroutines in Go?", ["Channels", "Global variables", "Pointers", "Signals"], 0),
        ("How does Go handle errors conventionally?", ["Functions return an explicit error value as the last return value", "Try/catch blocks", "Checked exceptions", "Exit codes"], 0),
    ],
    "Google Cloud": [
        ("Which Google Cloud service provides scalable, containerized microservices without server management?", ["Cloud Run", "Compute Engine", "Cloud Dataprep", "Cloud Composer"], 0),
        ("What is Google Cloud's globally distributed, highly scalable object storage service?", ["Cloud Storage", "Persistent Disk", "Filestore", "Cloud Memorystore"], 0),
        ("Which Google Cloud analytics warehouse allows querying petabytes of data using SQL?", ["BigQuery", "Cloud Bigtable", "Cloud Spanner", "Datastore"], 0),
    ],
    "GraphQL": [
        ("What is the primary advantage of GraphQL over traditional REST APIs?", ["Clients request exactly the data fields they need without over-fetching", "Faster network protocols", "Requires no schema", "Replaces database indexing"], 0),
        ("Which operation type in GraphQL is used to fetch or read data?", ["query", "mutation", "subscription", "action"], 0),
        ("Which GraphQL operation is used to create, update, or delete data on the server?", ["mutation", "query", "patch", "post"], 0),
    ],
    "Hadoop": [
        ("What is the distributed file system component of Apache Hadoop?", ["HDFS (Hadoop Distributed File System)", "S3", "NFS", "Ceph"], 0),
        ("Which computational programming model was historically used in Hadoop for batch processing?", ["MapReduce", "Spark Streaming", "MPI", "OpenMP"], 0),
        ("What is the resource management and job scheduling framework in Hadoop?", ["YARN", "Zookeeper", "HBase", "Pig"], 0),
    ],
    "Java": [
        ("Which component of Java converts bytecode into machine-specific native instructions at runtime?", ["JVM (Java Virtual Machine)", "JDK", "JAVAC compiler", "Javadoc"], 0),
        ("Which keyword is used to inherit a class in Java?", ["extends", "implements", "inherits", "using"], 0),
        ("Which collection class in Java implements a dynamic, resizable array?", ["ArrayList", "LinkedList", "HashMap", "TreeSet"], 0),
    ],
    "Jenkins": [
        ("What file name is conventionally used to define a Jenkins pipeline in source control?", ["Jenkinsfile", "pipeline.yml", "build.xml", "Jenkins.config"], 0),
        ("What are Jenkins Agents/Nodes used for?", ["Distributing and executing build jobs across multiple machines", "Managing user passwords", "Hosting the Jenkins web UI", "Storing git repositories"], 0),
        ("Which Jenkins pipeline section defines when a stage should execute?", ["when", "post", "environment", "triggers"], 0),
    ],
    "Jira": [
        ("In Jira, what is the fundamental unit of work used to track tasks, bugs, or user stories?", ["Issue", "Ticket", "Epic", "Card"], 0),
        ("Which Jira feature visually maps work stages (To Do, In Progress, Done) across columns?", ["Kanban / Scrum Board", "Roadmap", "Release Log", "Component Registry"], 0),
        ("What is the query language used in Jira to search for issues with custom filters?", ["JQL (Jira Query Language)", "SQL", "GraphQL", "Regex"], 0),
    ],
    "jQuery": [
        ("Which shorthand symbol is used to access the jQuery library?", ["$", "@", "#", "&"], 0),
        ("Which method is used in jQuery to make an asynchronous HTTP AJAX request?", ["$.ajax()", "$.fetch()", "$.http()", "$.getAsync()"], 0),
        ("How do you select an element with ID submit-btn using jQuery?", ["$('#submit-btn')", "$('.submit-btn')", "$('submit-btn')", "$('&submit-btn')"], 0),
    ],
    "Kotlin": [
        ("Which keyword is used to declare a read-only (immutable) variable in Kotlin?", ["val", "var", "const", "let"], 0),
        ("How does Kotlin handle null safety at compile time?", ["With built-in nullable types marked with '?'", "By banning null completely", "Using try-catch blocks automatically", "Via runtime reflection"], 0),
        ("What feature in Kotlin allows writing asynchronous, non-blocking code sequentially?", ["Coroutines", "Threads", "Goroutines", "Futures"], 0),
    ],
    "Laravel": [
        ("What is Laravel's built-in Object-Relational Mapper (ORM) called?", ["Eloquent", "Doctrine", "Hibernate", "ActiveRecord"], 0),
        ("What is the default templating engine in Laravel?", ["Blade", "Twig", "Smarty", "Jinja"], 0),
        ("Which command-line interface tool is included with Laravel for running migrations?", ["Artisan (php artisan)", "Composer", "Laravel CLI", "Drush"], 0),
    ],
    "MATLAB": [
        ("What is the fundamental data type in MATLAB, around which all operations are optimized?", ["Matrix / Array", "Linked List", "Dictionary", "Tuple"], 0),
        ("What is the default 1-based indexing convention in MATLAB for accessing the first element of vector v?", ["v(1)", "v[0]", "v(0)", "v.first()"], 0),
        ("Which MATLAB graphical environment is used for multidomain simulation and Model-Based Design?", ["Simulink", "Stateflow", "Guide", "App Designer"], 0),
    ],
    "Matplotlib": [
        ("Which module in Matplotlib provides a MATLAB-like plotting interface?", ["matplotlib.pyplot", "matplotlib.figure", "matplotlib.axes", "matplotlib.draw"], 0),
        ("Which command displays all currently created figures on the screen in Matplotlib?", ["plt.show()", "plt.render()", "plt.display()", "plt.open()"], 0),
        ("Which function creates a line plot of y versus x in Matplotlib?", ["plt.plot(x, y)", "plt.scatter(x, y)", "plt.line(x, y)", "plt.draw(x, y)"], 0),
    ],
    "MySQL": [
        ("What is the default relational storage engine in modern MySQL versions?", ["InnoDB", "MyISAM", "Memory", "Archive"], 0),
        ("Which clause is used in MySQL to sort result rows in ascending or descending order?", ["ORDER BY", "GROUP BY", "SORT BY", "ARRANGE BY"], 0),
        ("Which command displays the schema structure and column definitions of a table in MySQL?", ["DESCRIBE table_name;", "SHOW table_name;", "EXPLAIN ALL table_name;", "STRUCTURE table_name;"], 0),
    ],
    "Next.js": [
        ("What React-based framework enables server-side rendering (SSR) and static site generation (SSG)?", ["Next.js", "Express", "Vite", "Webpack"], 0),
        ("In modern Next.js (App Router), which directory handles file-system based routing?", ["app/", "pages/", "routes/", "src/components/"], 0),
        ("Which component is used in Next.js for client-side route transitions without full page reloads?", ["<Link href='...'>", "<a>", "<Route>", "<Navigate>"], 0),
    ],
    "Nginx": [
        ("What is Nginx primarily used for in modern web architectures?", ["Reverse proxy, load balancer, and high-performance static web server", "Relational database", "Programming language runtime", "Code compiler"], 0),
        ("Which configuration directive in Nginx is used to pass requests to a backend application server?", ["proxy_pass", "forward_to", "backend_redirect", "route_pass"], 0),
        ("Which command tests the syntax of Nginx configuration files without restarting the server?", ["nginx -t", "nginx -test", "nginx -check", "nginx -v"], 0),
    ],
    "NLP": [
        ("What does NLP stand for in Artificial Intelligence?", ["Natural Language Processing", "Neural Linguistic Program", "Network Language Protocol", "Node Language Parsing"], 0),
        ("What is the process of breaking a continuous text string into individual words or subwords?", ["Tokenization", "Stemming", "Lemmatization", "Vectorization"], 0),
        ("Which revolutionary neural network architecture introduced the self-attention mechanism in NLP?", ["Transformer", "CNN", "Decision Tree", "Perceptron"], 0),
    ],
    "OpenCV": [
        ("What is the default color channel ordering used when loading images in OpenCV via Python?", ["BGR", "RGB", "RGBA", "HSV"], 0),
        ("Which function in OpenCV reads an image file from disk?", ["cv2.imread()", "cv2.loadImage()", "cv2.open()", "cv2.read()"], 0),
        ("Which OpenCV algorithm is widely used to detect sharp edges in an image?", ["Canny edge detector", "Gaussian Blur", "Thresholding", "Harris Corner"], 0),
    ],
    "PHP": [
        ("What character must all variable names start with in PHP?", ["$", "@", "#", "var"], 0),
        ("Which superglobal array in PHP contains form data submitted via an HTTP POST request?", ["$_POST", "$_GET", "$_REQUEST_POST", "$_DATA"], 0),
        ("Which package manager is the standard dependency management tool for PHP?", ["Composer", "npm", "pip", "Bundler"], 0),
    ],
    "Postman": [
        ("What is Postman primarily used for by software developers?", ["Testing, designing, documenting, and debugging APIs", "Compiling backend source code", "Managing database schemas", "Hosting static web pages"], 0),
        ("In Postman, what feature allows grouping related API requests together with shared environment variables?", ["Collections", "Workflows", "Pipelines", "Clusters"], 0),
        ("What language is used in Postman to write automated pre-request scripts and test assertions?", ["JavaScript", "Python", "Ruby", "TypeScript"], 0),
    ],
    "Power BI": [
        ("What formula language is used in Power BI to create custom calculated columns and measures?", ["DAX (Data Analysis Expressions)", "SQL", "VBA", "Power Query M"], 0),
        ("What is the primary function of Power Query in Power BI?", ["Extracting, transforming, and loading (ETL) data from diverse sources", "Creating 3D charts", "Hosting cloud workspaces", "Managing database backups"], 0),
        ("What is a key difference between a Power BI Calculated Column and a Measure?", ["Calculated columns are computed row-by-row in storage; measures are evaluated on-the-fly dynamically", "Calculated columns only work on numbers", "Measures cannot be used in visuals", "They are identical in performance"], 0),
    ],
    "PyTorch": [
        ("What is the core multi-dimensional array object in PyTorch, similar to a NumPy ndarray?", ["torch.Tensor", "torch.Matrix", "torch.Array", "torch.Vector"], 0),
        ("What PyTorch engine automatically calculates gradients for neural network backpropagation?", ["Autograd", "AutoBackprop", "TorchGrad", "GradientFlow"], 0),
        ("Which PyTorch class is the base class for all neural network modules and layers?", ["torch.nn.Module", "torch.nn.Layer", "torch.Model", "torch.Network"], 0),
    ],
    "R": [
        ("What collection of R packages designed for data science includes ggplot2, dplyr, and tidyr?", ["Tidyverse", "SciPy", "RStudio Core", "CRAN Bundle"], 0),
        ("What is the standard assignment operator used in R?", ["<- (or =)", ":=", "==", "->"], 0),
        ("Which package in R is considered the industry standard for declarative data visualization?", ["ggplot2", "matplotlib", "plotR", "chartsR"], 0),
    ],
    "Redis": [
        ("What type of database is Redis primarily classified as?", ["In-memory key-value data store and cache", "Relational SQL database", "Document database", "Column-family database"], 0),
        ("Which Redis command is used to set a key with an automatic expiration time in seconds?", ["SETEX (or SET with EX)", "EXPIRE_SET", "TTL_SET", "TIMEOUT"], 0),
        ("What is Redis's typical read/write latency range due to keeping data in memory?", ["Sub-millisecond", "100-200ms", "5-10 seconds", "1-2 minutes"], 0),
    ],
    "REST API": [
        ("Which HTTP method is conventionally used in REST APIs to create a new resource?", ["POST", "GET", "DELETE", "OPTIONS"], 0),
        ("Which HTTP status code indicates that a resource was successfully created on the server?", ["201 Created", "200 OK", "204 No Content", "301 Moved Permanently"], 0),
        ("What is a core architectural constraint of REST regarding client-server interactions?", ["Statelessness: Each request from client must contain all info needed to process it", "Sessions must be stored in server memory", "Client and server must use same language", "All data must be XML"], 0),
    ],
    "Scikit-learn": [
        ("Which method is used across almost all Scikit-learn models to train on a dataset?", ["model.fit(X, y)", "model.train(X, y)", "model.learn(X, y)", "model.run(X, y)"], 0),
        ("Which function in Scikit-learn is used to split a dataset into training and testing sets?", ["train_test_split()", "split_data()", "cross_split()", "partition_data()"], 0),
        ("Which class in Scikit-learn is used to scale features so they have zero mean and unit variance?", ["StandardScaler", "MinMaxScaler", "RobustScaler", "Normalizer"], 0),
    ],
    "Seaborn": [
        ("What underlying plotting library is Seaborn built on top of in Python?", ["Matplotlib", "Plotly", "Bokeh", "D3.js"], 0),
        ("Which Seaborn function draws a scatter plot with an automatically calculated linear regression fit line?", ["sns.regplot() (or sns.lmplot())", "sns.lineplot()", "sns.scatterplot()", "sns.boxplot()"], 0),
        ("Which Seaborn plot is ideal for visualizing bivariate distributions and correlations across all pairs of numeric columns?", ["sns.pairplot()", "sns.heatmap()", "sns.violinplot()", "sns.catplot()"], 0),
    ],
    "Selenium": [
        ("What is Selenium primarily used for in software development?", ["Automating web browser interactions for end-to-end testing", "Compiling HTML and CSS", "Database query optimization", "Monitoring server CPU loads"], 0),
        ("Which component in Selenium connects test scripts to a specific browser like Chrome or Firefox?", ["WebDriver", "WebEngine", "Selenium Hub", "ProxyBridge"], 0),
        ("Which locator strategy in Selenium finds an element based on its unique HTML identifier attribute?", ["By.ID", "By.CLASS_NAME", "By.TAG_NAME", "By.LINK_TEXT"], 0),
    ],
    "Spark": [
        ("What was the original fundamental data abstraction in Apache Spark?", ["RDD (Resilient Distributed Dataset)", "Dataframe", "Array", "Series"], 0),
        ("Why is Apache Spark significantly faster than traditional Hadoop MapReduce for iterative workloads?", ["Spark processes and caches data in-memory across the cluster rather than reading/writing to disk", "Spark uses C++ while Hadoop uses Java", "Spark requires only a single machine", "Spark eliminates network serialization"], 0),
        ("What is the Python API library for Apache Spark called?", ["PySpark", "SparkPython", "PythonSpark", "SparkPy"], 0),
    ],
    "Spring Boot": [
        ("What feature in Spring Boot automatically configures beans based on the JAR dependencies in the classpath?", ["Auto-configuration", "Manual wiring", "XML Schema configuration", "Runtime reflection"], 0),
        ("What is the default embedded servlet container that comes bundled with Spring Boot web applications?", ["Apache Tomcat", "Jetty", "Undertow", "JBoss"], 0),
        ("Which annotation marks a class as a Spring RESTful controller handling HTTP requests?", ["@RestController", "@Controller", "@Service", "@Repository"], 0),
    ],
    "Statistics": [
        ("What measure of central tendency is calculated as the sum of all values divided by the count?", ["Mean", "Median", "Mode", "Variance"], 0),
        ("What does standard deviation measure in a dataset?", ["The dispersion / spread of data points relative to the mean", "The highest value", "The middle value", "The total count of observations"], 0),
        ("In hypothesis testing, what does a p-value less than alpha (typically 0.05) indicate?", ["Reject the null hypothesis (statistically significant result)", "Accept the null hypothesis", "Data has zero variance", "Sample size is invalid"], 0),
    ],
    "Swift": [
        ("Which keyword is used to declare an immutable constant in Swift?", ["let", "var", "const", "val"], 0),
        ("What Swift feature safely handles the absence of a value (wrapping either some value or nil)?", ["Optionals (?)", "Pointers", "Nullables", "Generics"], 0),
        ("What Apple framework was introduced to build declarative user interfaces across iOS and macOS with Swift?", ["SwiftUI", "UIKit", "AppKit", "Cocoa"], 0),
    ],
    "Tableau": [
        ("In Tableau, what is the difference between a Dimension and a Measure?", ["Dimensions contain qualitative/categorical values; Measures contain numeric quantitative values", "Dimensions are calculated fields only", "Measures can only be dates", "They are completely interchangeable"], 0),
        ("In Tableau, what color indicates a discrete field versus a continuous field in the pill shelf?", ["Blue for discrete, Green for continuous", "Green for discrete, Blue for continuous", "Red for discrete, Yellow for continuous", "Purple for discrete, Orange for continuous"], 0),
        ("What feature in Tableau combines multiple worksheets into a single interactive visual presentation?", ["Dashboard", "Storybook", "Worksheet", "Data Source"], 0),
    ],
    "Tailwind CSS": [
        ("What approach does Tailwind CSS take compared to traditional CSS frameworks like Bootstrap?", ["Utility-first: provides low-level utility classes directly in HTML markup", "Component-first: provides pre-built button and card classes only", "Inline CSS styling via style attributes", "CSS-in-JS runtime generation"], 0),
        ("In Tailwind CSS, how do you specify responsive styles for medium screens and above?", ["Prefix the class with md: (e.g. md:flex)", "Wrap in media query tags", "Use @media in class name", "Add .medium-screen suffix"], 0),
        ("Which configuration file is used in Tailwind CSS to customize theme colors, fonts, and plugins?", ["tailwind.config.js", "tailwind.json", "styles.config.css", "postcss.config.js"], 0),
    ],
    "Terraform": [
        ("What concept does HashiCorp Terraform implement to manage cloud infrastructure?", ["Infrastructure as Code (IaC)", "Continuous Integration (CI)", "Container Orchestration", "Server Monitoring"], 0),
        ("What file in Terraform keeps track of the current real-world state of your provisioned infrastructure?", ["terraform.tfstate", "terraform.lock.hcl", "main.tf", "variables.tf"], 0),
        ("Which command shows the execution plan of changes Terraform will make before applying them?", ["terraform plan", "terraform apply", "terraform validate", "terraform check"], 0),
    ],
    "Unit Testing": [
        ("What is the primary objective of a unit test in software engineering?", ["To test an individual isolated function or component in isolation from external dependencies", "To test the entire application end-to-end", "To test server network latency", "To evaluate database failover"], 0),
        ("What technique is used in unit testing to replace external dependencies (like databases or APIs) with simulated implementations?", ["Mocking / Stubbing", "Compiling", "Integration", "Refactoring"], 0),
        ("What popular, widely used testing framework in Python discovers test files prefixed with test_ automatically?", ["pytest", "unittest2", "pytester", "testrunner"], 0),
    ],
    "Vue.js": [
        ("What directive in Vue.js is used to bind an HTML input element two-way with component state?", ["v-model", "v-bind", "v-on", "v-sync"], 0),
        ("Which directive conditionally renders an element in the DOM based on the truthy value of an expression?", ["v-if", "v-show", "v-for", "v-switch"], 0),
        ("In Vue 3, what feature provides a function-based API for organizing component logic?", ["Composition API", "Options API", "Vuex Store", "Pinia Router"], 0),
    ],
}

# title, company, location, remote, level, min salary, max salary, skills, apply_link, contact_email, description
JOBS = [
    (
        "Python Software Engineer", "Canonical", "Remote", True, "junior", 8, 14,
        ["Python", "Linux", "Git", "Docker"],
        "https://canonical.com/careers", "careers@canonical.com",
        "Canonical, the publisher of Ubuntu, is looking for a Python Software Engineer to build and maintain cloud tooling and services. You will work across distributed systems, write automated tests, and contribute to open source software."
    ),
    (
        "Full Stack JavaScript / React Engineer", "Automattic", "Remote", True, "junior", 9, 16,
        ["JavaScript", "React", "HTML", "CSS", "Git", "REST API"],
        "https://automattic.com/work-with-us/", "jobs@automattic.com",
        "Automattic (creators of WordPress.com, WooCommerce, and Tumblr) is hiring a Full Stack React Engineer. Build intuitive web interfaces used by millions of bloggers and merchants worldwide."
    ),
    (
        "Backend Engineer (Go & Python)", "GitLab", "Remote", True, "mid", 14, 22,
        ["Python", "Docker", "Kubernetes", "Git", "CI/CD", "Linux"],
        "https://about.gitlab.com/jobs/", "talent@gitlab.com",
        "GitLab is an all-remote company building the complete DevSecOps platform. As a Backend Engineer, you will design scalable APIs, optimize database queries, and improve deployment pipelines."
    ),
    (
        "Data Analyst & Insights Specialist", "Spotify", "Remote", True, "fresher", 7, 12,
        ["SQL", "Python", "Pandas", "Tableau", "Statistics", "Power BI"],
        "https://www.lifeatspotify.com/jobs", "careers@spotify.com",
        "Join Spotify's analytics team to uncover listening trends and creator performance. You will query large datasets using SQL, build automated dashboards, and share actionable product metrics."
    ),
    (
        "Machine Learning & AI Engineer", "Hugging Face", "Remote", True, "junior", 12, 20,
        ["Python", "Machine Learning", "Deep Learning", "TensorFlow", "Pandas", "NumPy"],
        "https://huggingface.co/join", "jobs@huggingface.co",
        "Hugging Face is democratizing good machine learning. You will work on open-source transformer models, optimize inference on PyTorch and TensorFlow, and build community demos."
    ),
    (
        "Software Developer Intern", "Stripe", "Bangalore", False, "fresher", 8, 12,
        ["Python", "Java", "SQL", "Git"],
        "https://stripe.com/jobs", "recruiting@stripe.com",
        "Stripe is building economic infrastructure for the internet. Interns work alongside senior engineers to develop core payment flows, developer APIs, and high-reliability financial backends."
    ),
    (
        "Frontend Engineer (React / TypeScript)", "Razorpay", "Bangalore", False, "junior", 8, 15,
        ["React", "TypeScript", "JavaScript", "HTML", "CSS", "Git"],
        "https://jobs.lever.co/razorpay", "careers@razorpay.com",
        "Razorpay powers frictionless payments for businesses in India. In this role, you will build responsive, lightning-fast checkout experiences and financial dashboards with React and TypeScript."
    ),
    (
        "Junior Django / Python Developer", "Swiggy", "Bangalore", False, "junior", 7, 13,
        ["Python", "Django", "SQL", "REST API", "Git", "Redis"],
        "https://careers.swiggy.com", "campus@swiggy.in",
        "Swiggy connects consumers with millions of restaurants and stores. You will build microservices in Python and Django, handle peak delivery traffic, and optimize order dispatch algorithms."
    ),
    (
        "Data Science Intern", "Zomato", "Gurgaon", False, "fresher", 5, 8,
        ["Python", "Pandas", "SQL", "Statistics", "Machine Learning"],
        "https://www.zomato.com/careers", "jobs@zomato.com",
        "Work with Zomato's AI team to predict food delivery times, personalize restaurant recommendations, and build customer engagement models using Python, Pandas, and Scikit-Learn."
    ),
    (
        "Cloud & DevOps Engineer", "Docker", "Remote", True, "mid", 12, 20,
        ["Docker", "Kubernetes", "AWS", "Linux", "CI/CD", "Git"],
        "https://www.docker.com/careers/", "careers@docker.com",
        "Docker helps millions of developers build, share, and run containerized apps. You will maintain Kubernetes clusters, build CI/CD automation, and enhance developer tooling."
    ),
    (
        "Next.js Full Stack Engineer", "Vercel", "Remote", True, "mid", 15, 25,
        ["Next.js", "React", "TypeScript", "Node.js", "PostgreSQL"],
        "https://vercel.com/careers", "talent@vercel.com",
        "Vercel is the creator of Next.js and the frontend cloud platform. You will build world-class web experiences, work with edge compute, and push the boundaries of modern web development."
    ),
    (
        "Linux Systems & Cloud Associate", "Red Hat", "Pune", False, "fresher", 6, 10,
        ["Linux", "Bash", "Python", "Git", "C"],
        "https://www.redhat.com/en/jobs", "jobs@redhat.com",
        "Red Hat is the world's leading provider of enterprise open source solutions. You will collaborate on Red Hat Enterprise Linux, write automation scripts, and troubleshoot kernel and system services."
    ),
    (
        "Android Developer (Kotlin)", "Duolingo", "Remote", True, "junior", 10, 18,
        ["Kotlin", "Java", "Git", "REST API", "Firebase"],
        "https://careers.duolingo.com/", "jobs@duolingo.com",
        "Help make education free and accessible to everyone. Build gamified learning features for millions of Android users with Kotlin, Jetpack Compose, and clean MVVM architecture."
    ),
    (
        "Database & Backend Engineer", "MongoDB", "Gurgaon", False, "junior", 9, 16,
        ["MongoDB", "Node.js", "Python", "SQL", "Git"],
        "https://www.mongodb.com/careers", "campus@mongodb.com",
        "Join MongoDB to help developers unlock the power of data. You will work on document database drivers, build developer SDKs, and optimize high-throughput distributed database queries."
    ),
    (
        "QA Automation Engineer", "BrowserStack", "Mumbai", False, "junior", 7, 12,
        ["Selenium", "Python", "Unit Testing", "Git", "Jira"],
        "https://www.browserstack.com/careers", "careers@browserstack.com",
        "BrowserStack enables testing for over 50,000 customers worldwide. You will write robust Selenium automation scripts, integrate with CI/CD pipelines, and guarantee web and mobile app quality."
    ),
    (
        "C++ High Performance Programmer", "NVIDIA", "Pune", False, "mid", 16, 28,
        ["C++", "C", "Linux", "Git", "NumPy"],
        "https://www.nvidia.com/en-us/about-nvidia/careers/", "university@nvidia.com",
        "NVIDIA is the pioneer of GPU-accelerated computing. You will write high-performance C++ code, optimize compute kernels for AI acceleration, and work on system-level graphics software."
    ),
    (
        "Backend Node.js API Engineer", "Postman", "Bangalore", True, "junior", 9, 16,
        ["Node.js", "Express.js", "JavaScript", "REST API", "Git", "SQL"],
        "https://www.postman.com/company/careers/", "jobs@postman.com",
        "Postman is the leading API platform used by 30M+ developers. Help build and scale collaboration tools, mock servers, and API monitoring engines using Node.js and modern cloud architecture."
    ),
    (
        "Software Engineer - Azure Cloud", "Microsoft", "Hyderabad", False, "junior", 14, 24,
        ["Azure", "C#", ".NET", "SQL", "Git", "Docker"],
        "https://careers.microsoft.com/", "msjobs@microsoft.com",
        "Microsoft Azure provides scalable cloud solutions across the globe. You will develop cloud-native distributed microservices, enhance Azure services reliability, and write secure enterprise code."
    ),
    (
        "Associate Software Engineer", "Google", "Bangalore", False, "fresher", 15, 25,
        ["Python", "Java", "C++", "Git", "SQL"],
        "https://careers.google.com/", "googlejobs@google.com",
        "Google's engineering teams develop the next generation of technologies that empower billions. Fresh graduates collaborate with seasoned engineers to design scalable software, algorithms, and systems."
    ),
    (
        "Cloud Support Associate (AWS)", "Amazon", "Bangalore", False, "fresher", 7, 12,
        ["AWS", "Linux", "Bash", "Git"],
        "https://www.amazon.jobs/", "aws-careers@amazon.com",
        "Amazon Web Services (AWS) powers the cloud for startups and global enterprises. You will diagnose infrastructure issues, guide architects on cloud best practices, and automate customer deployments."
    ),
]

# jobs that should trigger the scam shield
SUSPICIOUS_JOBS = [
    {
        "title": "Work From Home Data Entry",
        "company": "QuickEarn Services",
        "location": "Remote",
        "level": "fresher",
        "min_salary": 20,
        "max_salary": 30,
        "contact_email": "quickearn.jobs@gmail.com",
        "description": "Earn big money from home with easy typing work. Pay a registration fee of 2000 to get your login. Guaranteed income every week.",
        "skills": [],
    },
    {
        "title": "Urgent Hiring Software Developer",
        "company": "GlobalSoft Pvt",
        "location": "Remote",
        "level": "fresher",
        "min_salary": 25,
        "max_salary": 40,
        "contact_email": "globalsoft.hr@yahoo.com",
        "description": "Immediate joining, no interview needed. A security deposit is required for the company laptop.",
        "skills": ["Python"],
    },
    {
        "title": "Data Analyst Trainee",
        "company": "Zenith Consulting",
        "location": "Delhi",
        "level": "fresher",
        "min_salary": 3,
        "max_salary": 4,
        "contact_email": "zenith.hr@gmail.com",
        "description": "Do various tasks as assigned by the manager.",
        "skills": ["SQL"],
    },
]
