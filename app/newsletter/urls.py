from django.urls import path
from . import views

app_name = "newsletter"
urlpatterns = [
    path("", views.index, name="index"),
    path("login_user", views.login_user, name="login"),
    path("signup", views.signup, name="signup"),
    path("login", views.login, name="signup"),
    path("profile", views.profile, name="profile"),
]