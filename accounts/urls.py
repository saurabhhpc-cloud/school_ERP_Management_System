from django.urls import path
from .views import user_login, post_login_redirect

app_name = "accounts"

urlpatterns = [
    path("login/", user_login, name="login"),
    path("post-login/", post_login_redirect, name="post_login"),
]
