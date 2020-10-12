from django.urls import path
from .import views

urlpatterns = [
    path('login', views.login, name="login"),
    path('signup', views.signup, name="signup"),
    path('logout', views.logout, name="logout"),
    path('emailConformation', views.emailConformation, name="emailConformation"),
    path('forgetPassword', views.forgetPassword, name="forgetPassword"),
    path('changepassword', views.changepassword, name="changepassword")
]
