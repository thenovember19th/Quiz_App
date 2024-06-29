from django.urls import path
from . import views

urlpatterns=[
    path('',views.home, name='home'),
    path('categories/', views.category_list, name='category_list'),
    path('category/<int:category_id>/', views.quiz_list, name='quiz_list'),
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('quiz/<int:quiz_id>/submit/', views.submit_quiz, name='submit_quiz'),
    path('quiz/<int:quiz_id>/results/', views.quiz_results, name='quiz_results'),
    path('signup/', views.signUp, name='signup'),
    path('customlogin/', views.custom_login, name='customlogin'),
    path('customlogout/', views.custom_logout, name='customlogout'),
]