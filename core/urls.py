from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Tutorials
    path('tutorials/', views.tutorial_list, name='tutorial_list'),
    path('tutorials/<str:language>/', views.tutorial_detail, name='tutorial_detail'),

    # Quiz — submit MUST come before <str:language> to avoid conflict
    path('quiz/', views.quiz_list, name='quiz_list'),
    path('quiz/submit/', views.submit_quiz, name='submit_quiz'),
    path('quiz/<str:language>/', views.quiz_detail, name='quiz_detail'),

    # Recommendations
    path('recommendations/', views.recommendations_view, name='recommendations'),
    path('recommendations/set-goal/', views.set_goal, name='set_goal'),

    # Admin
    path('admin-panel/', views.admin_panel, name='admin_panel'),
]
