from django.urls import path
from .views import *

urlpatterns = [
    path("send/request/", SendFriendRequest.as_view()),
    path("friends/list/", FriendsList.as_view()),
    path("pending/list/", PendingFriendsList.as_view()),
]
