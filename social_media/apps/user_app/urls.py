from django.urls import path
from .views import *

urlpatterns = [
    path("signUp/", UserSignUp.as_view()),
    path("login/", UserLogin.as_view()),
    path("logout/", UserLogout.as_view()),
    path("search/", SearchAPI.as_view()),
]
