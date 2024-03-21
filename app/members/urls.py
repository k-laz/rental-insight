from django.urls import path
from . import views


app_name = "members"
urlpatterns = [
    path('login_user', views.login_user, name="login_user"),
    path('logout_user', views.logout_user, name='logout_user'),
    path('register_user', views.register_user, name='register_user'),
    path('change_password', views.change_password, name="change_password"),
    path('reset_password', views.reset_password, name="reset_password"),
    path('delete_user', views.delete_user, name="delete_user"),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]

# Added by default
# members/login/ [name='login']
# members/logout/ [name='logout']
# members/password_change/ [name='password_change']
# members/password_change/done/ [name='password_change_done']
# members/password_reset/ [name='password_reset']
# members/password_reset/done/ [name='password_reset_done']
# members/reset/<uidb64>/<token>/ [name='password_reset_confirm']
# members/reset/done/ [name='password_reset_complete']