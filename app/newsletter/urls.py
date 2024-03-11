from django.urls import path
from . import views

app_name = "newsletter"
urlpatterns = [
    path("", views.index, name="index"),
    # path("login_user", views.login_user, name="login_user"),
    # path("register_user", views.register_user, name="register_user"),
    path("profile", views.profile, name="profile"),
    path("register_filter", views.register_filter, name="register_filter"),
    path("send_mail", views.send_aggregated_daily_newsletters, name="send_mail"),
]