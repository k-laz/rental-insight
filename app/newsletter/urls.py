from django.urls import path
from . import views

app_name = "newsletter"
urlpatterns = [
    path("", views.index, name="index"),
    path("login_user", views.login_user, name="login"),
    path("sign_up", views.sign_up, name="sign_up"),
    path("profile", views.profile, name="profile"),
]