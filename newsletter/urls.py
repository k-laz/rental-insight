from django.urls import path
from . import views

app_name = "newsletter"
urlpatterns = [
    path("", views.home, name="home"),
    path("filters", views.filters, name="filters"),
    path("listings", views.listings, name="listings"),
    path("settings", views.settings, name="settings"),
    path("send_mail", views.send_aggregated_daily_newsletters, name="send_mail"),
]