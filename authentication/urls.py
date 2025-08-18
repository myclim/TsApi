from django.urls import path
from authentication.views import *

app_name = "user"

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="user-login"),
    path("register/", UserRegisterView.as_view(), name="user-register"),
    path("update/", UserUpdateView.as_view(), name="user-update"),
    path("delete/", UserDeleteView.as_view(), name="user-delete"),
]