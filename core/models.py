from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('normal', 'Normal User'),
        ('admin', 'Admin'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='normal')
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"

    def is_admin_user(self):
        return self.user_type == 'admin'


class QuizQuestion(models.Model):
    LANGUAGE_CHOICES = [
        ('python', 'Python'),
        ('django', 'Django'),
        ('java', 'Java'),
        ('springboot', 'Spring Boot'),
        ('html', 'HTML'),
        ('css', 'CSS'),
        ('javascript', 'JavaScript'),
        ('react', 'React'),
        ('nodejs', 'Node.js'),
        ('sql', 'SQL'),
    ]
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES)
    question = models.TextField()
    option_a = models.CharField(max_length=300)
    option_b = models.CharField(max_length=300)
    option_c = models.CharField(max_length=300)
    option_d = models.CharField(max_length=300)
    correct_answer = models.CharField(max_length=1, choices=[('A','A'),('B','B'),('C','C'),('D','D')])
    explanation = models.TextField(blank=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.language.upper()}] {self.question[:60]}"


class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    selected_answer = models.CharField(max_length=1)
    is_correct = models.BooleanField()
    attempted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.question.language} - {'✓' if self.is_correct else '✗'}"


class CourseRecommendation(models.Model):
    GOAL_CHOICES = [
        ('fullstack', 'Full Stack Developer'),
        ('frontend', 'Frontend Developer'),
        ('backend', 'Backend Developer'),
        ('data_analyst', 'Data Analyst'),
        ('data_scientist', 'Data Scientist'),
        ('devops', 'DevOps Engineer'),
        ('mobile', 'Mobile Developer'),
        ('ml_engineer', 'ML Engineer'),
    ]
    goal = models.CharField(max_length=30, choices=GOAL_CHOICES)
    recommended_languages = models.JSONField()  # list of language keys
    description = models.TextField()
    roadmap = models.JSONField(default=list)  # ordered list of steps

    def __str__(self):
        return self.goal


class UserGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal = models.CharField(max_length=30)
    selected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} → {self.goal}"
