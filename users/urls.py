from typing import List

from django.urls import path
from django.contrib.auth import views as av

from .views import user_register

urlpatterns: List = [
    path("login/", av.LoginView.as_view(
        template_name="user_login.html"
    ), name="user_login"),
    path("logout/", av.LogoutView.as_view(
        template_name="user_logout.html"
    ), name="user_logout"),
    path("register/", user_register, name="user_register"),
]