from django.db import models
from apps.user_app.models import User
# Create your models here.


class FriendsRequestTracker(models.Model):
    PENDING = 0
    ACCEPT = 1
    REJECT = -1
    receiver = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="sent_requests")
    sender = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="receive_requests")
    status = models.IntegerField(default=PENDING)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)