from django.contrib import admin
from .models import UserProfile, QuizQuestion, QuizAttempt, CourseRecommendation, UserGoal

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user_type', 'created_at']
    list_filter = ['user_type']

@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ['language', 'question', 'correct_answer', 'difficulty']
    list_filter = ['language', 'difficulty']
    search_fields = ['question']

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'question', 'selected_answer', 'is_correct', 'attempted_at']
    list_filter = ['is_correct', 'question__language']

@admin.register(UserGoal)
class UserGoalAdmin(admin.ModelAdmin):
    list_display = ['user', 'goal', 'selected_at']
