from django.core.management.base import BaseCommand
from core.models import QuizQuestion


QUESTIONS = [
    # PYTHON
    {'language': 'python', 'question': 'What is the output of print(type([]))?', 'option_a': "<class 'list'>", 'option_b': "<class 'array'>", 'option_c': "<type 'list'>", 'option_d': 'list', 'correct_answer': 'A', 'explanation': 'In Python 3, type([]) returns <class "list">.', 'difficulty': 'easy'},
    {'language': 'python', 'question': 'Which keyword is used to define a function in Python?', 'option_a': 'function', 'option_b': 'def', 'option_c': 'func', 'option_d': 'define', 'correct_answer': 'B', 'explanation': 'Python uses the "def" keyword to define functions.', 'difficulty': 'easy'},
    {'language': 'python', 'question': 'What does len("Hello") return?', 'option_a': '4', 'option_b': '6', 'option_c': '5', 'option_d': '7', 'correct_answer': 'C', 'explanation': '"Hello" has 5 characters.', 'difficulty': 'easy'},
    {'language': 'python', 'question': 'Which data structure uses key-value pairs in Python?', 'option_a': 'List', 'option_b': 'Tuple', 'option_c': 'Set', 'option_d': 'Dictionary', 'correct_answer': 'D', 'explanation': 'Dictionaries in Python store data as key-value pairs.', 'difficulty': 'easy'},
    {'language': 'python', 'question': 'What is the result of 10 // 3 in Python?', 'option_a': '3.33', 'option_b': '3', 'option_c': '4', 'option_d': '1', 'correct_answer': 'B', 'explanation': '// is floor division which returns 3 for 10 // 3.', 'difficulty': 'easy'},
    {'language': 'python', 'question': 'Which method is used to add an element to a list?', 'option_a': 'add()', 'option_b': 'insert()', 'option_c': 'append()', 'option_d': 'push()', 'correct_answer': 'C', 'explanation': 'list.append() adds an element to the end of a list.', 'difficulty': 'easy'},
    {'language': 'python', 'question': 'What does the "self" keyword refer to in Python?', 'option_a': 'The class itself', 'option_b': 'The instance of the class', 'option_c': 'A static method', 'option_d': 'A global variable', 'correct_answer': 'B', 'explanation': '"self" refers to the current instance of the class.', 'difficulty': 'medium'},
    {'language': 'python', 'question': 'What is a lambda function in Python?', 'option_a': 'A named function', 'option_b': 'A class method', 'option_c': 'An anonymous function', 'option_d': 'A generator function', 'correct_answer': 'C', 'explanation': 'Lambda functions are small anonymous functions defined with the lambda keyword.', 'difficulty': 'medium'},

    # DJANGO
    {'language': 'django', 'question': 'Which command creates a new Django project?', 'option_a': 'django-admin startapp', 'option_b': 'django-admin startproject', 'option_c': 'python manage.py startproject', 'option_d': 'django new project', 'correct_answer': 'B', 'explanation': 'django-admin startproject creates a new Django project.', 'difficulty': 'easy'},
    {'language': 'django', 'question': 'Which file contains URL patterns in Django?', 'option_a': 'views.py', 'option_b': 'models.py', 'option_c': 'urls.py', 'option_d': 'settings.py', 'correct_answer': 'C', 'explanation': 'URL patterns are defined in urls.py in Django.', 'difficulty': 'easy'},
    {'language': 'django', 'question': 'Which ORM method retrieves all records from a model?', 'option_a': 'Model.find_all()', 'option_b': 'Model.objects.all()', 'option_c': 'Model.get_all()', 'option_d': 'Model.select()', 'correct_answer': 'B', 'explanation': 'Model.objects.all() returns a QuerySet of all objects.', 'difficulty': 'easy'},
    {'language': 'django', 'question': 'What does CSRF stand for in Django?', 'option_a': 'Cross-Site Request Forgery', 'option_b': 'Client-Side Request Forgery', 'option_c': 'Cross-Script Resource Filter', 'option_d': 'Common Security Request Feature', 'correct_answer': 'A', 'explanation': 'CSRF stands for Cross-Site Request Forgery - a security protection in Django forms.', 'difficulty': 'medium'},
    {'language': 'django', 'question': 'Which Django class is used to create database tables?', 'option_a': 'django.db.Table', 'option_b': 'django.models.Schema', 'option_c': 'django.db.models.Model', 'option_d': 'django.db.Entity', 'correct_answer': 'C', 'explanation': 'Models inherit from django.db.models.Model to represent database tables.', 'difficulty': 'easy'},
    {'language': 'django', 'question': 'What is the purpose of migrations in Django?', 'option_a': 'To move files between folders', 'option_b': 'To propagate model changes to the database', 'option_c': 'To migrate users between systems', 'option_d': 'To transfer data between databases', 'correct_answer': 'B', 'explanation': 'Migrations track and apply changes to your database schema.', 'difficulty': 'medium'},

    # JAVA
    {'language': 'java', 'question': 'Which keyword is used to inherit a class in Java?', 'option_a': 'implements', 'option_b': 'inherits', 'option_c': 'extends', 'option_d': 'super', 'correct_answer': 'C', 'explanation': 'The "extends" keyword is used for class inheritance in Java.', 'difficulty': 'easy'},
    {'language': 'java', 'question': 'What is the default value of an int variable in Java?', 'option_a': 'null', 'option_b': '1', 'option_c': 'undefined', 'option_d': '0', 'correct_answer': 'D', 'explanation': 'The default value for int in Java is 0.', 'difficulty': 'easy'},
    {'language': 'java', 'question': 'Which method is the entry point of a Java program?', 'option_a': 'start()', 'option_b': 'main()', 'option_c': 'run()', 'option_d': 'init()', 'correct_answer': 'B', 'explanation': 'public static void main(String[] args) is the entry point.', 'difficulty': 'easy'},
    {'language': 'java', 'question': 'What does JVM stand for?', 'option_a': 'Java Verified Machine', 'option_b': 'Java Virtual Machine', 'option_c': 'Java Variable Manager', 'option_d': 'Java Visual Module', 'correct_answer': 'B', 'explanation': 'JVM stands for Java Virtual Machine which executes Java bytecode.', 'difficulty': 'easy'},
    {'language': 'java', 'question': 'Which collection allows duplicate elements in Java?', 'option_a': 'HashSet', 'option_b': 'TreeSet', 'option_c': 'ArrayList', 'option_d': 'LinkedHashSet', 'correct_answer': 'C', 'explanation': 'ArrayList allows duplicate elements unlike Set implementations.', 'difficulty': 'medium'},
    {'language': 'java', 'question': 'What is an interface in Java?', 'option_a': 'A class with only static methods', 'option_b': 'A blueprint with abstract methods', 'option_c': 'A type of variable', 'option_d': 'An abstract class with constructors', 'correct_answer': 'B', 'explanation': 'An interface is a blueprint containing abstract methods that classes must implement.', 'difficulty': 'medium'},

    # SPRING BOOT
    {'language': 'springboot', 'question': 'Which annotation marks a class as a Spring component?', 'option_a': '@Bean', 'option_b': '@Component', 'option_c': '@Service', 'option_d': '@Autowired', 'correct_answer': 'B', 'explanation': '@Component is the generic annotation for any Spring-managed component.', 'difficulty': 'easy'},
    {'language': 'springboot', 'question': 'Which annotation is used to create a REST controller?', 'option_a': '@Controller', 'option_b': '@RestController', 'option_c': '@RequestMapping', 'option_d': '@Service', 'correct_answer': 'B', 'explanation': '@RestController combines @Controller and @ResponseBody for REST APIs.', 'difficulty': 'easy'},
    {'language': 'springboot', 'question': 'What is the default port for Spring Boot applications?', 'option_a': '3000', 'option_b': '8080', 'option_c': '80', 'option_d': '5000', 'correct_answer': 'B', 'explanation': 'Spring Boot runs on port 8080 by default.', 'difficulty': 'easy'},
    {'language': 'springboot', 'question': 'Which annotation handles GET requests in Spring Boot?', 'option_a': '@PostMapping', 'option_b': '@RequestMapping', 'option_c': '@GetMapping', 'option_d': '@FetchMapping', 'correct_answer': 'C', 'explanation': '@GetMapping is a shortcut for @RequestMapping(method = RequestMethod.GET).', 'difficulty': 'easy'},
    {'language': 'springboot', 'question': 'What does @Autowired do in Spring Boot?', 'option_a': 'Creates a new bean', 'option_b': 'Marks a class as a controller', 'option_c': 'Injects a bean automatically', 'option_d': 'Defines a REST endpoint', 'correct_answer': 'C', 'explanation': '@Autowired enables automatic dependency injection.', 'difficulty': 'medium'},

    # HTML
    {'language': 'html', 'question': 'What does HTML stand for?', 'option_a': 'Hyper Text Markup Language', 'option_b': 'High Text Machine Language', 'option_c': 'Hyper Transfer Markup Language', 'option_d': 'Home Tool Markup Language', 'correct_answer': 'A', 'explanation': 'HTML stands for HyperText Markup Language.', 'difficulty': 'easy'},
    {'language': 'html', 'question': 'Which tag is used to create a hyperlink?', 'option_a': '<link>', 'option_b': '<url>', 'option_c': '<href>', 'option_d': '<a>', 'correct_answer': 'D', 'explanation': 'The <a> (anchor) tag is used to create hyperlinks.', 'difficulty': 'easy'},
    {'language': 'html', 'question': 'Which attribute specifies an image URL?', 'option_a': 'link', 'option_b': 'src', 'option_c': 'href', 'option_d': 'url', 'correct_answer': 'B', 'explanation': 'The src attribute specifies the URL of the image.', 'difficulty': 'easy'},
    {'language': 'html', 'question': 'Which tag creates the largest heading?', 'option_a': '<h6>', 'option_b': '<head>', 'option_c': '<h1>', 'option_d': '<heading>', 'correct_answer': 'C', 'explanation': '<h1> creates the largest heading in HTML.', 'difficulty': 'easy'},
    {'language': 'html', 'question': 'What is the purpose of the <meta> tag?', 'option_a': 'Creates navigation menus', 'option_b': 'Defines page metadata', 'option_c': 'Embeds media', 'option_d': 'Creates tables', 'correct_answer': 'B', 'explanation': 'The <meta> tag defines metadata about the HTML document.', 'difficulty': 'medium'},
    {'language': 'html', 'question': 'Which tag is used for an unordered list?', 'option_a': '<ol>', 'option_b': '<dl>', 'option_c': '<list>', 'option_d': '<ul>', 'correct_answer': 'D', 'explanation': '<ul> creates an unordered (bulleted) list.', 'difficulty': 'easy'},

    # CSS
    {'language': 'css', 'question': 'What does CSS stand for?', 'option_a': 'Creative Style Sheets', 'option_b': 'Computer Style Sheets', 'option_c': 'Cascading Style Sheets', 'option_d': 'Colorful Style Sheets', 'correct_answer': 'C', 'explanation': 'CSS stands for Cascading Style Sheets.', 'difficulty': 'easy'},
    {'language': 'css', 'question': 'Which property changes the text color in CSS?', 'option_a': 'text-color', 'option_b': 'font-color', 'option_c': 'foreground', 'option_d': 'color', 'correct_answer': 'D', 'explanation': 'The "color" property sets the text color.', 'difficulty': 'easy'},
    {'language': 'css', 'question': 'Which CSS property controls element visibility without removing it?', 'option_a': 'display: none', 'option_b': 'opacity: 0', 'option_c': 'visibility: hidden', 'option_d': 'hidden: true', 'correct_answer': 'C', 'explanation': 'visibility: hidden hides the element but keeps its space.', 'difficulty': 'medium'},
    {'language': 'css', 'question': 'What is the box model in CSS?', 'option_a': 'A 3D element layout', 'option_b': 'Content, padding, border, and margin areas', 'option_c': 'Grid layout system', 'option_d': 'Flexbox container', 'correct_answer': 'B', 'explanation': 'The CSS box model consists of content, padding, border, and margin.', 'difficulty': 'medium'},
    {'language': 'css', 'question': 'Which value of display creates a flex container?', 'option_a': 'display: inline', 'option_b': 'display: box', 'option_c': 'display: flex', 'option_d': 'display: grid-flex', 'correct_answer': 'C', 'explanation': 'display: flex creates a flex container for flexbox layouts.', 'difficulty': 'easy'},

    # JAVASCRIPT
    {'language': 'javascript', 'question': 'Which keyword declares a block-scoped variable?', 'option_a': 'var', 'option_b': 'let', 'option_c': 'const', 'option_d': 'Both let and const', 'correct_answer': 'D', 'explanation': 'Both let and const are block-scoped (const is also immutable).', 'difficulty': 'medium'},
    {'language': 'javascript', 'question': 'What does typeof null return in JavaScript?', 'option_a': '"null"', 'option_b': '"undefined"', 'option_c': '"object"', 'option_d': '"nothing"', 'correct_answer': 'C', 'explanation': 'typeof null returns "object" - this is a known JavaScript bug.', 'difficulty': 'hard'},
    {'language': 'javascript', 'question': 'Which method adds an event listener in JavaScript?', 'option_a': 'element.on()', 'option_b': 'element.listen()', 'option_c': 'element.bind()', 'option_d': 'element.addEventListener()', 'correct_answer': 'D', 'explanation': 'addEventListener() attaches an event handler to an element.', 'difficulty': 'easy'},
    {'language': 'javascript', 'question': 'What is a Promise in JavaScript?', 'option_a': 'A synchronous operation', 'option_b': 'An object representing eventual completion of async operation', 'option_c': 'A type of loop', 'option_d': 'A variable declaration', 'correct_answer': 'B', 'explanation': 'A Promise represents the eventual completion or failure of an asynchronous operation.', 'difficulty': 'medium'},
    {'language': 'javascript', 'question': 'Which method converts a JSON string to a JS object?', 'option_a': 'JSON.stringify()', 'option_b': 'JSON.convert()', 'option_c': 'JSON.decode()', 'option_d': 'JSON.parse()', 'correct_answer': 'D', 'explanation': 'JSON.parse() converts a JSON string to a JavaScript object.', 'difficulty': 'easy'},

    # REACT
    {'language': 'react', 'question': 'What is JSX in React?', 'option_a': 'JavaScript XML syntax extension', 'option_b': 'A CSS framework', 'option_c': 'A testing library', 'option_d': 'A state management tool', 'correct_answer': 'A', 'explanation': 'JSX is a syntax extension for JavaScript that looks similar to HTML.', 'difficulty': 'easy'},
    {'language': 'react', 'question': 'Which hook is used for side effects in React?', 'option_a': 'useState', 'option_b': 'useContext', 'option_c': 'useEffect', 'option_d': 'useReducer', 'correct_answer': 'C', 'explanation': 'useEffect is used for side effects like data fetching, subscriptions, etc.', 'difficulty': 'medium'},
    {'language': 'react', 'question': 'What does useState return?', 'option_a': 'A single value', 'option_b': 'An array with state and setter function', 'option_c': 'An object', 'option_d': 'A Promise', 'correct_answer': 'B', 'explanation': 'useState returns [state, setState] - the current state and a function to update it.', 'difficulty': 'easy'},

    # NODE.JS
    {'language': 'nodejs', 'question': 'Which command initializes a new Node.js project?', 'option_a': 'node init', 'option_b': 'npm start', 'option_c': 'npm init', 'option_d': 'node create', 'correct_answer': 'C', 'explanation': 'npm init creates a package.json file for a new Node.js project.', 'difficulty': 'easy'},
    {'language': 'nodejs', 'question': 'Which module is built into Node.js for HTTP operations?', 'option_a': 'express', 'option_b': 'http', 'option_c': 'web', 'option_d': 'net', 'correct_answer': 'B', 'explanation': 'The "http" module is a built-in Node.js module for HTTP functionality.', 'difficulty': 'easy'},
    {'language': 'nodejs', 'question': 'What is npm?', 'option_a': 'Node Package Manager', 'option_b': 'New Project Manager', 'option_c': 'Node Process Manager', 'option_d': 'Network Protocol Manager', 'correct_answer': 'A', 'explanation': 'npm stands for Node Package Manager.', 'difficulty': 'easy'},

    # SQL
    {'language': 'sql', 'question': 'Which SQL command retrieves data from a table?', 'option_a': 'GET', 'option_b': 'FETCH', 'option_c': 'SELECT', 'option_d': 'READ', 'correct_answer': 'C', 'explanation': 'SELECT is used to retrieve data from a database table.', 'difficulty': 'easy'},
    {'language': 'sql', 'question': 'Which clause filters records in SQL?', 'option_a': 'HAVING', 'option_b': 'FILTER', 'option_c': 'WHERE', 'option_d': 'LIMIT', 'correct_answer': 'C', 'explanation': 'The WHERE clause filters records based on a condition.', 'difficulty': 'easy'},
    {'language': 'sql', 'question': 'What does JOIN do in SQL?', 'option_a': 'Deletes rows from a table', 'option_b': 'Combines rows from multiple tables', 'option_c': 'Creates a new table', 'option_d': 'Groups rows by column', 'correct_answer': 'B', 'explanation': 'JOIN combines rows from two or more tables based on a related column.', 'difficulty': 'easy'},
    {'language': 'sql', 'question': 'Which function counts the number of rows?', 'option_a': 'SUM()', 'option_b': 'TOTAL()', 'option_c': 'COUNT()', 'option_d': 'NUMBER()', 'correct_answer': 'C', 'explanation': 'COUNT() returns the number of rows matching the query.', 'difficulty': 'easy'},
    {'language': 'sql', 'question': 'What is the difference between DELETE and TRUNCATE?', 'option_a': 'No difference', 'option_b': 'DELETE removes specific rows; TRUNCATE removes all rows', 'option_c': 'TRUNCATE removes specific rows; DELETE removes all', 'option_d': 'DELETE is faster', 'correct_answer': 'B', 'explanation': 'DELETE can remove specific rows with WHERE; TRUNCATE removes all rows quickly.', 'difficulty': 'medium'},
]


class Command(BaseCommand):
    help = 'Seed quiz questions into the database'

    def handle(self, *args, **kwargs):
        count = 0
        for q in QUESTIONS:
            obj, created = QuizQuestion.objects.get_or_create(
                language=q['language'],
                question=q['question'],
                defaults=q
            )
            if created:
                count += 1
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {count} quiz questions.'))
