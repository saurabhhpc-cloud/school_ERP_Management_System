from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import user_login, post_login_redirect


urlpatterns = [
    path("login/", user_login, name="login"),
    path("post-login/", post_login_redirect, name="post-login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
