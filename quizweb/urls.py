from django.urls import path
from quizweb import views

urlpatterns=[
    path('register/',views.RegistrationView.as_view(),name='register'),
    path('signin/',views.SignInView.as_view(),name='signin'),
    path('home/',views.IndexView.as_view(),name='home'),
    path('quiz/home/',views.QuizHomeView.as_view(),name='quiz-home'),
    path('questions/all/<str:cat>/<str:mode>/',views.QuestionListView.as_view(),name='questions-list'),
    path('quiz/record/',views.QuizRecordView.as_view(),name='quiz-record'),
    path('signout/',views.signout_view,name='signout'),


]