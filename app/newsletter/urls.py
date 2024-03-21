from django.urls import path
from . import views

app_name = "newsletter"
urlpatterns = [
    path("", views.home, name="home"),
    path("profile", views.profile, name="profile"),
    path("send_mail", views.send_aggregated_daily_newsletters, name="send_mail"),
]