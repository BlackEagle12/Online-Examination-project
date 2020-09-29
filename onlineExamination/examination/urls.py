from django.urls import path
from .import views

urlpatterns = [
    path('exams', views.exams, name="exams"),
    path('results', views.results, name="results"),
    path('exam', views.exam, name="exam"),
    path('continue_exam', views.continue_exam, name="continue_exam"),
]