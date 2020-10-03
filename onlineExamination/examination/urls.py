from django.urls import path
from .import views

urlpatterns = [
    path('exams', views.exams, name="exams"),
    path('results', views.results, name="results"),
    path('exam', views.exam, name="exam"),
    path('result', views.result, name="result"),
    path('continue_exam', views.continue_exam, name="continue_exam"),
    path('attempt_quiz', views.attempt_quiz, name="attempt_quiz"),
    path('testView', views.testView, name="testView")
]