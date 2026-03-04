from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

from .models import UserProfile, QuizQuestion, QuizAttempt, CourseRecommendation, UserGoal


# ─────────────────── HOME ───────────────────
def home(request):
    return render(request, 'core/home.html')


# ─────────────────── AUTH ───────────────────
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        user_type = request.POST.get('user_type', 'normal')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'core/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'core/register.html')

        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters.')
            return render(request, 'core/register.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        if user_type == 'admin':
            user.is_staff = True
            user.save()

        UserProfile.objects.create(user=user, user_type=user_type)
        login(request, user)
        messages.success(request, f'Welcome, {username}! Account created successfully.')
        return redirect('dashboard')

    return render(request, 'core/register.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


# ─────────────────── DASHBOARD ───────────────────
@login_required
def dashboard(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    total_attempts = QuizAttempt.objects.filter(user=request.user).count()
    correct_attempts = QuizAttempt.objects.filter(user=request.user, is_correct=True).count()
    score_pct = round((correct_attempts / total_attempts * 100), 1) if total_attempts else 0

    languages = [
        {'key': 'python', 'name': 'Python', 'icon': '🐍', 'color': '#3776ab', 'desc': 'General-purpose programming language'},
        {'key': 'django', 'name': 'Django', 'icon': '🌿', 'color': '#092e20', 'desc': 'High-level Python Web framework'},
        {'key': 'java', 'name': 'Java', 'icon': '☕', 'color': '#f89820', 'desc': 'Object-oriented programming language'},
        {'key': 'springboot', 'name': 'Spring Boot', 'icon': '🍃', 'color': '#6db33f', 'desc': 'Java-based production-grade framework'},
        {'key': 'html', 'name': 'HTML', 'icon': '🌐', 'color': '#e34c26', 'desc': 'Markup language for web pages'},
        {'key': 'css', 'name': 'CSS', 'icon': '🎨', 'color': '#264de4', 'desc': 'Styling language for web pages'},
        {'key': 'javascript', 'name': 'JavaScript', 'icon': '⚡', 'color': '#f7df1e', 'desc': 'Dynamic programming for the web'},
        {'key': 'react', 'name': 'React', 'icon': '⚛️', 'color': '#61dafb', 'desc': 'JavaScript library for UIs'},
        {'key': 'nodejs', 'name': 'Node.js', 'icon': '🟢', 'color': '#339933', 'desc': 'JavaScript runtime environment'},
        {'key': 'sql', 'name': 'SQL', 'icon': '🗄️', 'color': '#f29111', 'desc': 'Database query language'},
    ]

    context = {
        'profile': profile,
        'languages': languages,
        'total_attempts': total_attempts,
        'correct_attempts': correct_attempts,
        'score_pct': score_pct,
    }
    return render(request, 'core/dashboard.html', context)


# ─────────────────── TUTORIALS ───────────────────
TUTORIAL_DATA = {
    'python': {
        'name': 'Python',
        'icon': '🐍',
        'color': '#3776ab',
        'bg_gradient': 'linear-gradient(135deg, #3776ab, #ffd43b)',
        'description': 'Python is a versatile, beginner-friendly programming language used in web development, data science, AI, automation, and more.',
        'resources': [
            {'title': 'W3Schools Python Tutorial', 'url': 'https://www.w3schools.com/python/', 'icon': '📘', 'desc': 'Comprehensive beginner-friendly Python tutorial with examples'},
            {'title': 'GeeksForGeeks Python', 'url': 'https://www.geeksforgeeks.org/python-programming-language/', 'icon': '🟢', 'desc': 'In-depth Python programming articles and practice problems'},
            {'title': 'Python Official Docs', 'url': 'https://docs.python.org/3/', 'icon': '📖', 'desc': 'Official Python 3 documentation and language reference'},
            {'title': 'Real Python', 'url': 'https://realpython.com/', 'icon': '🎯', 'desc': 'Practical Python tutorials for all skill levels'},
            {'title': 'Python.org Beginners Guide', 'url': 'https://wiki.python.org/moin/BeginnersGuide', 'icon': '🚀', 'desc': 'Official beginners guide to Python programming'},
            {'title': 'Programiz Python', 'url': 'https://www.programiz.com/python-programming', 'icon': '💡', 'desc': 'Learn Python with simple examples and exercises'},
        ],
        'topics': ['Variables & Data Types', 'Control Flow', 'Functions', 'OOP', 'File Handling', 'Modules & Packages', 'Exception Handling', 'List Comprehensions', 'Decorators', 'Generators'],
    },
    'django': {
        'name': 'Django',
        'icon': '🌿',
        'color': '#092e20',
        'bg_gradient': 'linear-gradient(135deg, #092e20, #44b78b)',
        'description': 'Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design.',
        'resources': [
            {'title': 'Django Official Docs', 'url': 'https://docs.djangoproject.com/', 'icon': '📖', 'desc': 'Official Django documentation - the best starting point'},
            {'title': 'W3Schools Django', 'url': 'https://www.w3schools.com/django/', 'icon': '📘', 'desc': 'Django tutorial with practical examples'},
            {'title': 'GeeksForGeeks Django', 'url': 'https://www.geeksforgeeks.org/django-tutorial/', 'icon': '🟢', 'desc': 'Step-by-step Django tutorial for beginners'},
            {'title': 'Django Girls Tutorial', 'url': 'https://tutorial.djangogirls.org/', 'icon': '💜', 'desc': 'Friendly Django tutorial to build your first web app'},
            {'title': 'Real Python Django', 'url': 'https://realpython.com/tutorials/django/', 'icon': '🎯', 'desc': 'Practical Django development tutorials'},
            {'title': 'Mozilla MDN Django', 'url': 'https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django', 'icon': '🦊', 'desc': 'MDN Web Docs Django server-side guide'},
        ],
        'topics': ['Django Setup', 'Models & ORM', 'Views & URLs', 'Templates', 'Forms', 'Authentication', 'Admin Panel', 'REST APIs', 'Django ORM Queries', 'Deployment'],
    },
    'java': {
        'name': 'Java',
        'icon': '☕',
        'color': '#f89820',
        'bg_gradient': 'linear-gradient(135deg, #f89820, #e63946)',
        'description': 'Java is a class-based, object-oriented programming language designed to have as few implementation dependencies as possible.',
        'resources': [
            {'title': 'W3Schools Java', 'url': 'https://www.w3schools.com/java/', 'icon': '📘', 'desc': 'Learn Java syntax and concepts step by step'},
            {'title': 'GeeksForGeeks Java', 'url': 'https://www.geeksforgeeks.org/java/', 'icon': '🟢', 'desc': 'Java programming with examples and interview questions'},
            {'title': 'Oracle Java Docs', 'url': 'https://docs.oracle.com/javase/', 'icon': '📖', 'desc': 'Official Java SE documentation from Oracle'},
            {'title': 'Programiz Java', 'url': 'https://www.programiz.com/java-programming', 'icon': '💡', 'desc': 'Java tutorials with interactive examples'},
            {'title': 'Javatpoint Java', 'url': 'https://www.javatpoint.com/java-tutorial', 'icon': '🎓', 'desc': 'Comprehensive Java tutorial for beginners and professionals'},
            {'title': 'Baeldung Java', 'url': 'https://www.baeldung.com/', 'icon': '🔷', 'desc': 'Java and Spring ecosystem tutorials'},
        ],
        'topics': ['Java Basics', 'OOP Concepts', 'Collections Framework', 'Exception Handling', 'Multithreading', 'File I/O', 'Generics', 'Lambda Expressions', 'Streams API', 'JDBC'],
    },
    'springboot': {
        'name': 'Spring Boot',
        'icon': '🍃',
        'color': '#6db33f',
        'bg_gradient': 'linear-gradient(135deg, #6db33f, #1a1a2e)',
        'description': 'Spring Boot makes it easy to create stand-alone, production-grade Spring-based applications that you can just run.',
        'resources': [
            {'title': 'Spring Official Docs', 'url': 'https://spring.io/projects/spring-boot', 'icon': '📖', 'desc': 'Official Spring Boot documentation and guides'},
            {'title': 'Baeldung Spring Boot', 'url': 'https://www.baeldung.com/spring-boot', 'icon': '🔷', 'desc': 'Extensive Spring Boot tutorials and examples'},
            {'title': 'GeeksForGeeks Spring Boot', 'url': 'https://www.geeksforgeeks.org/spring-boot/', 'icon': '🟢', 'desc': 'Spring Boot concepts with practical examples'},
            {'title': 'Javatpoint Spring Boot', 'url': 'https://www.javatpoint.com/spring-boot-tutorial', 'icon': '🎓', 'desc': 'Step-by-step Spring Boot tutorial'},
            {'title': 'Spring Guides', 'url': 'https://spring.io/guides', 'icon': '🍃', 'desc': 'Official Spring getting-started guides'},
            {'title': 'Tutorialspoint Spring Boot', 'url': 'https://www.tutorialspoint.com/spring_boot/', 'icon': '📚', 'desc': 'Comprehensive Spring Boot reference'},
        ],
        'topics': ['Spring Boot Basics', 'Auto Configuration', 'REST APIs', 'Spring Data JPA', 'Spring Security', 'Actuator', 'Microservices', 'Spring MVC', 'Testing', 'Deployment'],
    },
    'html': {
        'name': 'HTML',
        'icon': '🌐',
        'color': '#e34c26',
        'bg_gradient': 'linear-gradient(135deg, #e34c26, #f7941d)',
        'description': 'HTML (HyperText Markup Language) is the standard markup language for creating web pages and web applications.',
        'resources': [
            {'title': 'W3Schools HTML', 'url': 'https://www.w3schools.com/html/', 'icon': '📘', 'desc': 'The most popular HTML tutorial on the web'},
            {'title': 'Mozilla MDN HTML', 'url': 'https://developer.mozilla.org/en-US/docs/Web/HTML', 'icon': '🦊', 'desc': 'Comprehensive HTML reference and guides by Mozilla'},
            {'title': 'GeeksForGeeks HTML', 'url': 'https://www.geeksforgeeks.org/html-tutorial/', 'icon': '🟢', 'desc': 'HTML tutorials with examples and exercises'},
            {'title': 'HTML.com', 'url': 'https://html.com/', 'icon': '🌐', 'desc': 'Modern HTML guide for beginners'},
            {'title': 'freeCodeCamp HTML', 'url': 'https://www.freecodecamp.org/learn/responsive-web-design/', 'icon': '🔥', 'desc': 'Free interactive HTML & CSS course'},
            {'title': 'Tutorialspoint HTML', 'url': 'https://www.tutorialspoint.com/html/', 'icon': '📚', 'desc': 'HTML5 reference guide with live editor'},
        ],
        'topics': ['HTML Structure', 'Tags & Elements', 'Forms & Input', 'Tables', 'Semantic HTML', 'HTML5 APIs', 'Media Elements', 'Canvas', 'SVG', 'Accessibility'],
    },
    'css': {
        'name': 'CSS',
        'icon': '🎨',
        'color': '#264de4',
        'bg_gradient': 'linear-gradient(135deg, #264de4, #c43ad6)',
        'description': 'CSS (Cascading Style Sheets) is used to describe how HTML elements should be displayed on screen, paper, or other media.',
        'resources': [
            {'title': 'W3Schools CSS', 'url': 'https://www.w3schools.com/css/', 'icon': '📘', 'desc': 'Complete CSS reference with live examples'},
            {'title': 'Mozilla MDN CSS', 'url': 'https://developer.mozilla.org/en-US/docs/Web/CSS', 'icon': '🦊', 'desc': 'Official CSS documentation and tutorials'},
            {'title': 'CSS-Tricks', 'url': 'https://css-tricks.com/', 'icon': '✨', 'desc': 'Tips, tricks, and techniques on using CSS'},
            {'title': 'GeeksForGeeks CSS', 'url': 'https://www.geeksforgeeks.org/css-tutorial/', 'icon': '🟢', 'desc': 'CSS tutorials from basics to advanced'},
            {'title': 'Flexbox Froggy', 'url': 'https://flexboxfroggy.com/', 'icon': '🐸', 'desc': 'Learn CSS flexbox interactively'},
            {'title': 'Grid Garden', 'url': 'https://cssgridgarden.com/', 'icon': '🥕', 'desc': 'Learn CSS Grid layout interactively'},
        ],
        'topics': ['Selectors', 'Box Model', 'Flexbox', 'CSS Grid', 'Animations', 'Transitions', 'Media Queries', 'Variables', 'Pseudo-classes', 'CSS Frameworks'],
    },
    'javascript': {
        'name': 'JavaScript',
        'icon': '⚡',
        'color': '#f7df1e',
        'bg_gradient': 'linear-gradient(135deg, #f7df1e, #ff6b35)',
        'description': 'JavaScript is the programming language of the web, enabling interactive and dynamic content on websites.',
        'resources': [
            {'title': 'W3Schools JavaScript', 'url': 'https://www.w3schools.com/js/', 'icon': '📘', 'desc': 'Learn JavaScript from scratch'},
            {'title': 'Mozilla MDN JavaScript', 'url': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript', 'icon': '🦊', 'desc': 'Comprehensive JavaScript documentation'},
            {'title': 'JavaScript.info', 'url': 'https://javascript.info/', 'icon': '📗', 'desc': 'Modern JavaScript tutorial - the best JS guide'},
            {'title': 'GeeksForGeeks JS', 'url': 'https://www.geeksforgeeks.org/javascript/', 'icon': '🟢', 'desc': 'JavaScript tutorials and interview questions'},
            {'title': 'freeCodeCamp JS', 'url': 'https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/', 'icon': '🔥', 'desc': 'Free JavaScript certification course'},
            {'title': 'Eloquent JavaScript', 'url': 'https://eloquentjavascript.net/', 'icon': '📕', 'desc': 'Free book on modern JavaScript programming'},
        ],
        'topics': ['Variables & Types', 'Functions', 'DOM Manipulation', 'Events', 'Async/Await', 'Promises', 'ES6+ Features', 'Closures', 'Prototypes', 'Modules'],
    },
    'react': {
        'name': 'React',
        'icon': '⚛️',
        'color': '#61dafb',
        'bg_gradient': 'linear-gradient(135deg, #61dafb, #20232a)',
        'description': 'React is a JavaScript library for building fast, interactive user interfaces for web and mobile apps.',
        'resources': [
            {'title': 'React Official Docs', 'url': 'https://react.dev/', 'icon': '📖', 'desc': 'Official React documentation with interactive examples'},
            {'title': 'W3Schools React', 'url': 'https://www.w3schools.com/react/', 'icon': '📘', 'desc': 'React tutorial for beginners'},
            {'title': 'GeeksForGeeks React', 'url': 'https://www.geeksforgeeks.org/reactjs/', 'icon': '🟢', 'desc': 'React.js tutorials and projects'},
            {'title': 'Scrimba React Course', 'url': 'https://scrimba.com/learn/learnreact', 'icon': '🎮', 'desc': 'Interactive React course'},
            {'title': 'freeCodeCamp React', 'url': 'https://www.freecodecamp.org/learn/front-end-development-libraries/#react', 'icon': '🔥', 'desc': 'Free React certification'},
            {'title': 'React Tutorial', 'url': 'https://react-tutorial.app/', 'icon': '🚀', 'desc': 'Step-by-step interactive React tutorial'},
        ],
        'topics': ['Components', 'JSX', 'Props & State', 'Hooks', 'Context API', 'React Router', 'useEffect', 'Redux', 'Performance', 'Testing'],
    },
    'nodejs': {
        'name': 'Node.js',
        'icon': '🟢',
        'color': '#339933',
        'bg_gradient': 'linear-gradient(135deg, #339933, #1a1a2e)',
        'description': 'Node.js is a JavaScript runtime built on Chrome\'s V8 engine that lets you run JavaScript server-side.',
        'resources': [
            {'title': 'Node.js Official Docs', 'url': 'https://nodejs.org/en/docs/', 'icon': '📖', 'desc': 'Official Node.js documentation'},
            {'title': 'W3Schools Node.js', 'url': 'https://www.w3schools.com/nodejs/', 'icon': '📘', 'desc': 'Node.js tutorial for beginners'},
            {'title': 'GeeksForGeeks Node.js', 'url': 'https://www.geeksforgeeks.org/nodejs/', 'icon': '🟢', 'desc': 'Node.js tutorials and examples'},
            {'title': 'The Odin Project Node', 'url': 'https://www.theodinproject.com/paths/full-stack-javascript', 'icon': '⚔️', 'desc': 'Full-stack JavaScript with Node.js'},
            {'title': 'Express.js Guide', 'url': 'https://expressjs.com/en/guide/routing.html', 'icon': '🚂', 'desc': 'Official Express.js framework guide'},
            {'title': 'NodeSchool', 'url': 'https://nodeschool.io/', 'icon': '🏫', 'desc': 'Open source workshops for learning Node.js'},
        ],
        'topics': ['Node Basics', 'npm/yarn', 'Express.js', 'File System', 'HTTP Module', 'Async Programming', 'Streams', 'REST APIs', 'Authentication', 'MongoDB with Node'],
    },
    'sql': {
        'name': 'SQL',
        'icon': '🗄️',
        'color': '#f29111',
        'bg_gradient': 'linear-gradient(135deg, #f29111, #e63946)',
        'description': 'SQL (Structured Query Language) is the standard language for managing and manipulating relational databases.',
        'resources': [
            {'title': 'W3Schools SQL', 'url': 'https://www.w3schools.com/sql/', 'icon': '📘', 'desc': 'Complete SQL tutorial with live editor'},
            {'title': 'GeeksForGeeks SQL', 'url': 'https://www.geeksforgeeks.org/sql-tutorial/', 'icon': '🟢', 'desc': 'SQL tutorials with examples and exercises'},
            {'title': 'SQLZoo', 'url': 'https://sqlzoo.net/', 'icon': '🦁', 'desc': 'Interactive SQL tutorial with exercises'},
            {'title': 'Mode SQL Tutorial', 'url': 'https://mode.com/sql-tutorial/', 'icon': '📊', 'desc': 'SQL for data analysis tutorial'},
            {'title': 'Khan Academy SQL', 'url': 'https://www.khanacademy.org/computing/computer-programming/sql', 'icon': '🎓', 'desc': 'Free interactive SQL course'},
            {'title': 'LeetCode SQL', 'url': 'https://leetcode.com/problemset/database/', 'icon': '💻', 'desc': 'Practice SQL with real interview problems'},
        ],
        'topics': ['SELECT Queries', 'WHERE Clause', 'JOINs', 'GROUP BY', 'Subqueries', 'Indexes', 'Stored Procedures', 'Transactions', 'Views', 'Database Design'],
    },
}


@login_required
def tutorial_list(request):
    languages = [
        {'key': k, 'name': v['name'], 'icon': v['icon'], 'color': v['color'], 'desc': v['description'][:100] + '...'}
        for k, v in TUTORIAL_DATA.items()
    ]
    return render(request, 'core/tutorial_list.html', {'languages': languages})


@login_required
def tutorial_detail(request, language):
    data = TUTORIAL_DATA.get(language)
    if not data:
        return redirect('tutorial_list')
    return render(request, 'core/tutorial_detail.html', {'data': data, 'language': language})


# ─────────────────── QUIZ ───────────────────
@login_required
def quiz_list(request):
    languages = list(TUTORIAL_DATA.keys())
    lang_info = [{'key': k, 'name': TUTORIAL_DATA[k]['name'], 'icon': TUTORIAL_DATA[k]['icon'],
                  'color': TUTORIAL_DATA[k]['color'],
                  'count': QuizQuestion.objects.filter(language=k).count()}
                 for k in languages]
    return render(request, 'core/quiz_list.html', {'languages': lang_info})


@login_required
def quiz_detail(request, language):
    data = TUTORIAL_DATA.get(language)
    if not data:
        return redirect('quiz_list')
    questions = list(QuizQuestion.objects.filter(language=language).values(
        "id", "language", "question", "option_a", "option_b", "option_c", "option_d",
        "correct_answer", "explanation", "difficulty"
    ))
    context = {
        'language': language,
        'language_name': data['name'],
        'language_icon': data['icon'],
        'language_color': data['color'],
        'questions_json': json.dumps(questions),
        'question_count': len(questions),
    }
    return render(request, 'core/quiz_detail.html', context)


@login_required
@require_POST
def submit_quiz(request):
    data = json.loads(request.body)
    language = data.get('language')
    answers = data.get('answers', {})
    results = []
    score = 0

    for qid_str, selected in answers.items():
        try:
            q = QuizQuestion.objects.get(id=int(qid_str))
            is_correct = q.correct_answer == selected
            if is_correct:
                score += 1
            QuizAttempt.objects.create(
                user=request.user,
                question=q,
                selected_answer=selected,
                is_correct=is_correct,
            )
            results.append({
                'id': q.id,
                'correct': is_correct,
                'correct_answer': q.correct_answer,
                'explanation': q.explanation,
            })
        except QuizQuestion.DoesNotExist:
            pass

    return JsonResponse({'score': score, 'total': len(answers), 'results': results})


# ─────────────────── RECOMMENDATIONS ───────────────────
RECOMMENDATIONS = {
    'fullstack': {
        'title': 'Full Stack Developer',
        'emoji': '🚀',
        'description': 'A Full Stack Developer works on both frontend (UI) and backend (server/database). You\'ll need strong skills in web technologies.',
        'roadmap': [
            {'step': 1, 'title': 'HTML & CSS Fundamentals', 'desc': 'Learn to build and style web pages', 'icon': '🌐', 'duration': '3-4 weeks'},
            {'step': 2, 'title': 'JavaScript', 'desc': 'Add interactivity and dynamic behavior', 'icon': '⚡', 'duration': '6-8 weeks'},
            {'step': 3, 'title': 'Python or Java (Backend)', 'desc': 'Choose your backend language', 'icon': '🐍', 'duration': '6-8 weeks'},
            {'step': 4, 'title': 'Django or Spring Boot', 'desc': 'Learn a web framework for your backend', 'icon': '🌿', 'duration': '6-8 weeks'},
            {'step': 5, 'title': 'React (Frontend Framework)', 'desc': 'Build modern single-page applications', 'icon': '⚛️', 'duration': '6-8 weeks'},
            {'step': 6, 'title': 'SQL & Databases', 'desc': 'Learn to store and query data', 'icon': '🗄️', 'duration': '3-4 weeks'},
            {'step': 7, 'title': 'Node.js', 'desc': 'Optional: JavaScript backend', 'icon': '🟢', 'duration': '4-6 weeks'},
        ],
        'languages': ['html', 'css', 'javascript', 'python', 'django', 'react', 'sql', 'nodejs'],
    },
    'frontend': {
        'title': 'Frontend Developer',
        'emoji': '🎨',
        'description': 'Frontend Developers build what users see and interact with. Focus on UI, UX, and visual design.',
        'roadmap': [
            {'step': 1, 'title': 'HTML', 'desc': 'Web page structure', 'icon': '🌐', 'duration': '2-3 weeks'},
            {'step': 2, 'title': 'CSS', 'desc': 'Styling, animations, layouts', 'icon': '🎨', 'duration': '4-6 weeks'},
            {'step': 3, 'title': 'JavaScript', 'desc': 'DOM manipulation and ES6+', 'icon': '⚡', 'duration': '8-10 weeks'},
            {'step': 4, 'title': 'React', 'desc': 'Component-based UI development', 'icon': '⚛️', 'duration': '6-8 weeks'},
            {'step': 5, 'title': 'Node.js', 'desc': 'Build tools and package management', 'icon': '🟢', 'duration': '2-3 weeks'},
        ],
        'languages': ['html', 'css', 'javascript', 'react', 'nodejs'],
    },
    'backend': {
        'title': 'Backend Developer',
        'emoji': '⚙️',
        'description': 'Backend Developers build server-side logic, APIs, and database systems that power web applications.',
        'roadmap': [
            {'step': 1, 'title': 'Python or Java', 'desc': 'Choose your primary backend language', 'icon': '🐍', 'duration': '6-8 weeks'},
            {'step': 2, 'title': 'SQL & Databases', 'desc': 'PostgreSQL, MySQL fundamentals', 'icon': '🗄️', 'duration': '4-6 weeks'},
            {'step': 3, 'title': 'Django or Spring Boot', 'desc': 'Web framework for APIs', 'icon': '🌿', 'duration': '6-8 weeks'},
            {'step': 4, 'title': 'Node.js', 'desc': 'REST APIs with Express.js', 'icon': '🟢', 'duration': '4-6 weeks'},
            {'step': 5, 'title': 'Java Advanced', 'desc': 'Microservices and enterprise patterns', 'icon': '☕', 'duration': '8-10 weeks'},
        ],
        'languages': ['python', 'java', 'django', 'springboot', 'sql', 'nodejs'],
    },
    'data_analyst': {
        'title': 'Data Analyst',
        'emoji': '📊',
        'description': 'Data Analysts examine datasets, identify trends, and present insights to help businesses make decisions.',
        'roadmap': [
            {'step': 1, 'title': 'Python', 'desc': 'Pandas, NumPy for data manipulation', 'icon': '🐍', 'duration': '6-8 weeks'},
            {'step': 2, 'title': 'SQL', 'desc': 'Query and extract data from databases', 'icon': '🗄️', 'duration': '4-6 weeks'},
            {'step': 3, 'title': 'Java (Optional)', 'desc': 'Big data tools like Apache Spark', 'icon': '☕', 'duration': '4-6 weeks'},
            {'step': 4, 'title': 'Data Visualization', 'desc': 'Matplotlib, Seaborn, Tableau', 'icon': '📈', 'duration': '3-4 weeks'},
            {'step': 5, 'title': 'Statistics & Math', 'desc': 'Statistical analysis and probability', 'icon': '📐', 'duration': '4-6 weeks'},
        ],
        'languages': ['python', 'sql', 'java'],
    },
    'data_scientist': {
        'title': 'Data Scientist',
        'emoji': '🧬',
        'description': 'Data Scientists build ML models, apply statistical methods, and extract deep insights from complex datasets.',
        'roadmap': [
            {'step': 1, 'title': 'Python', 'desc': 'Core language for data science and ML', 'icon': '🐍', 'duration': '8-10 weeks'},
            {'step': 2, 'title': 'SQL', 'desc': 'Data extraction and management', 'icon': '🗄️', 'duration': '3-4 weeks'},
            {'step': 3, 'title': 'Machine Learning', 'desc': 'Scikit-learn, TensorFlow, PyTorch', 'icon': '🤖', 'duration': '10-12 weeks'},
            {'step': 4, 'title': 'Statistics & Math', 'desc': 'Linear algebra, calculus, probability', 'icon': '📐', 'duration': '6-8 weeks'},
            {'step': 5, 'title': 'Big Data Tools', 'desc': 'Spark, Hadoop, cloud platforms', 'icon': '☁️', 'duration': '4-6 weeks'},
        ],
        'languages': ['python', 'sql', 'java'],
    },
    'devops': {
        'title': 'DevOps Engineer',
        'emoji': '🔧',
        'description': 'DevOps Engineers bridge development and operations, focusing on automation, CI/CD, and cloud infrastructure.',
        'roadmap': [
            {'step': 1, 'title': 'Python', 'desc': 'Scripting and automation', 'icon': '🐍', 'duration': '4-6 weeks'},
            {'step': 2, 'title': 'Java', 'desc': 'Enterprise application understanding', 'icon': '☕', 'duration': '4-6 weeks'},
            {'step': 3, 'title': 'Shell Scripting', 'desc': 'Bash scripting for automation', 'icon': '🖥️', 'duration': '3-4 weeks'},
            {'step': 4, 'title': 'Docker & Kubernetes', 'desc': 'Containerization and orchestration', 'icon': '🐳', 'duration': '6-8 weeks'},
            {'step': 5, 'title': 'CI/CD Pipelines', 'desc': 'Jenkins, GitHub Actions, GitLab', 'icon': '🔄', 'duration': '4-6 weeks'},
        ],
        'languages': ['python', 'java', 'sql'],
    },
    'mobile': {
        'title': 'Mobile Developer',
        'emoji': '📱',
        'description': 'Mobile Developers build iOS and Android applications for smartphones and tablets.',
        'roadmap': [
            {'step': 1, 'title': 'Java or Kotlin', 'desc': 'Android native development', 'icon': '🤖', 'duration': '8-10 weeks'},
            {'step': 2, 'title': 'JavaScript + React Native', 'desc': 'Cross-platform mobile apps', 'icon': '⚛️', 'duration': '6-8 weeks'},
            {'step': 3, 'title': 'HTML & CSS', 'desc': 'Hybrid app development basics', 'icon': '🌐', 'duration': '3-4 weeks'},
            {'step': 4, 'title': 'SQL', 'desc': 'Mobile database management (SQLite)', 'icon': '🗄️', 'duration': '2-3 weeks'},
            {'step': 5, 'title': 'REST APIs', 'desc': 'Connecting mobile apps to backends', 'icon': '🔗', 'duration': '3-4 weeks'},
        ],
        'languages': ['java', 'javascript', 'react', 'html', 'css', 'sql'],
    },
    'ml_engineer': {
        'title': 'ML Engineer',
        'emoji': '🤖',
        'description': 'ML Engineers design, build, and deploy machine learning systems in production environments.',
        'roadmap': [
            {'step': 1, 'title': 'Python', 'desc': 'Primary language for ML/AI', 'icon': '🐍', 'duration': '8-10 weeks'},
            {'step': 2, 'title': 'Mathematics', 'desc': 'Linear algebra, calculus, statistics', 'icon': '📐', 'duration': '8-10 weeks'},
            {'step': 3, 'title': 'ML Frameworks', 'desc': 'TensorFlow, PyTorch, Scikit-learn', 'icon': '🧠', 'duration': '10-12 weeks'},
            {'step': 4, 'title': 'SQL & Data Engineering', 'desc': 'Data pipelines and storage', 'icon': '🗄️', 'duration': '4-6 weeks'},
            {'step': 5, 'title': 'Java (Big Data)', 'desc': 'Spark, Hadoop for large-scale ML', 'icon': '☕', 'duration': '4-6 weeks'},
            {'step': 6, 'title': 'MLOps & Deployment', 'desc': 'Model serving, monitoring, pipelines', 'icon': '🚀', 'duration': '6-8 weeks'},
        ],
        'languages': ['python', 'java', 'sql'],
    },
}


@login_required
def recommendations_view(request):
    user_goal = None
    try:
        user_goal = UserGoal.objects.filter(user=request.user).latest('selected_at')
    except UserGoal.DoesNotExist:
        pass

    rec_data = None
    if user_goal and user_goal.goal in RECOMMENDATIONS:
        rec_data = RECOMMENDATIONS[user_goal.goal]
        rec_data['_goal_key'] = user_goal.goal

    goals = [
        {'key': k, 'title': v['title'], 'emoji': v['emoji'], 'desc': v['description'][:80] + '...'}
        for k, v in RECOMMENDATIONS.items()
    ]

    context = {
        'goals': goals,
        'user_goal': user_goal,
        'rec_data': rec_data,
        'tutorial_data': json.dumps({k: {'name': v['name'], 'icon': v['icon']} for k, v in TUTORIAL_DATA.items()}),
    }
    return render(request, 'core/recommendations.html', context)


@login_required
@require_POST
def set_goal(request):
    data = json.loads(request.body)
    goal = data.get('goal', '')
    if goal in RECOMMENDATIONS:
        UserGoal.objects.create(user=request.user, goal=goal)
        return JsonResponse({'status': 'ok', 'rec': RECOMMENDATIONS[goal]})
    return JsonResponse({'status': 'error'}, status=400)


# ─────────────────── ADMIN PANEL ───────────────────
@login_required
def admin_panel(request):
    try:
        profile = request.user.profile
        if not profile.is_admin_user() and not request.user.is_superuser:
            messages.error(request, 'Access denied. Admin only.')
            return redirect('dashboard')
    except UserProfile.DoesNotExist:
        if not request.user.is_superuser:
            messages.error(request, 'Access denied. Admin only.')
            return redirect('dashboard')

    users = User.objects.all().select_related('profile')
    total_questions = QuizQuestion.objects.count()
    total_attempts = QuizAttempt.objects.count()
    languages_stats = {}
    for lang_key in TUTORIAL_DATA.keys():
        count = QuizQuestion.objects.filter(language=lang_key).count()
        attempts = QuizAttempt.objects.filter(question__language=lang_key).count()
        languages_stats[lang_key] = {'name': TUTORIAL_DATA[lang_key]['name'], 'questions': count, 'attempts': attempts}

    context = {
        'users': users,
        'total_questions': total_questions,
        'total_attempts': total_attempts,
        'languages_stats': languages_stats,
    }
    return render(request, 'core/admin_panel.html', context)
