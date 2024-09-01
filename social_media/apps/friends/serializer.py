from rest_framework import serializers
from .models import FriendsRequestTracker


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendsRequestTracker
        fields = ("sender", "receiver", "status",)
