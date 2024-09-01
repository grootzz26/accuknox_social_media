
from apps.common.base import *
from ..common import common_serializer
from ..common.base import AppViewMixin, AppCreateAPIView, AppListAPIView, require_loggedin_user
from django.db.models import Q
from .models import FriendsRequestTracker
from .serializer import FriendRequestSerializer
from django.core.cache import cache
from apps.user_app.models import User


class SendFriendRequest(AppCreateAPIView):
    
    serializer_class = FriendRequestSerializer
    
    @require_loggedin_user
    def post(self, request):
        auth = self.get_auth_data(request)
        action_code = request.GET.get("action", None)
        if action_code == "send":
            cache_key = "apps.friend_request_limit.{}".format(auth.token)
            count = cache.get(cache_key)
            if count and count >= 3:
                return self.send_error_response(message="You crossed limit. you are not able to send more than 3 request within a minute!")
            data = dict(sender=auth.user, receiver = self.get_user())
            connect = FriendsRequestTracker.objects.filter(**data).last()
            if connect and connect.status == 0:
                return self.send_error_response(message=f"You've already sent request to {data['receiver'].email}")
            elif connect and connect.status == 1:
                return self.send_error_response(message=f"You already connected with {data['receiver'].email}")
            if not connect:
                FriendsRequestTracker.objects.create(**data)
            if count and count<=3:
                count += 1
                try:
                    ttl = cache.ttl(cache_key)
                    cache.set(cache_key, count, ttl)
                except:
                    cache.set(cache_key, 1, 60)
            else:
                cache.set(cache_key, 1, 60)
            return self.send_response(message=f"SENT_FRIEND_REQUEST_TO_{data['receiver'].email}")
        elif action_code == "accept":
            receiver = auth.user
            sender = self.get_user()
            tracker = FriendsRequestTracker.objects.filter(sender=sender, receiver=receiver).select_related("sender", "receiver").last()
            if tracker and tracker.status == 0:
                tracker.status = 1
                tracker.save()
                return self.send_response(message=f"FRIEND_REQUEST_ACCEPTED_{tracker.sender.email}")
            elif tracker.status == 1:
                return self.send_error_response(message="You already accepted this friend request")
            else:
                return self.send_error_response(message="You already rejected this friend request")
        else:
            receiver = auth.user
            sender = self.get_user()
            tracker = FriendsRequestTracker.objects.filter(sender=sender, receiver=receiver).select_related("sender", "receiver").last()
            if tracker and not tracker.status == -1:
                tracker.status = -1
                tracker.save()
                return self.send_response(message=f"FRIEND_REQUEST_REJECTED_{tracker.sender.email}")
            elif tracker.status == -1:
                return self.send_error_response(message="You already rejected this friend request")
            else:
                return self.send_error_response(message="Friend Not found")




class FriendsList(AppListAPIView):

    @require_loggedin_user
    def get(self, request):
        auth = self.get_auth_data(request)
        friends = FriendsRequestTracker.objects.filter(Q(receiver=auth.user) | Q(sender=auth.user),
                                                       status=1).select_related("sender", "receiver")
        data = []
        for f in friends:
            user = f.receiver if f.sender == auth.user else f.sender
            serializer = common_serializer(User, meta_fields=["id", "name", "email"])(user)
            data.append(serializer.data)
        return self.send_response(data=data, message="FRIENDS_FETCHED")


class PendingFriendsList(AppListAPIView):

    @require_loggedin_user
    def get(self, request):
        auth = self.get_auth_data(request)
        friends = FriendsRequestTracker.objects.filter(receiver=auth.user, status=0)
        data = []
        for f in friends:
            serializer = common_serializer(User, meta_fields=["id", "name", "email"])(f.sender)
            data.append(serializer.data)
        return self.send_response(data=data, message="PENDING_LIST")
