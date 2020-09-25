from django.urls import path
from .import views

urlpatterns = [
    path('home', redirect('/home')),
    path('home', views.home, name="home")
]