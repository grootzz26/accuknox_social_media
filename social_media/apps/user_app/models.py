
from django.db import models
from django.utils import timezone
from datetime import datetime


# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=120, null=True, blank=True)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=254, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email


class Token(models.Model):
    LOGOUT = 0
    LOGIN = 1
    token = models.CharField(max_length=254, null=True, blank=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    status = models.IntegerField(default=LOGOUT)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        default_related_name = "related_user_token"

    def __str__(self):
        return self.token + " --- " + self.user.email
