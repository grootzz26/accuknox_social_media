from django.shortcuts import render
from apps.common.base import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import CreateAPIView
import json
from .serializers import *
from ..common import common_serializer
from ..common.base import AppViewMixin, AppCreateAPIView, AppListAPIView, require_loggedin_user
from django.db.models import Q
from .pagination import *



# Create your views here.


class UserSignUp(AppCreateAPIView, AppViewMixin):

    serializer_class = SignUpSerializer

    def post(self, request):
        serializer = self.get_valid_serializer()
        user = serializer.save()
        token = Token.objects.create(token=generate_auth_token(), user=user)
        response = common_serializer(User, meta_fields=["name", "email"])(user).data
        response["user_token"] = token.token
        return self.send_response(response, message="USER_REGISTERED")


class UserLogin(AppCreateAPIView):

    serializer_class = SignInSerializer

    def post(self, request):
        self.get_valid_serializer()
        user = self.get_user()
        breakpoint()
        auth = user.related_user_token.all()[0]
        if auth.status:
            message = "User already Logged in"
            return self.send_error_response(message=message)
        auth.status = 1
        auth.save()
        data = {
            "email": user.email,
            "auth_token": auth.token
        }
        return self.send_response(data, message="USER_LOGGED_IN", action_code="NEED_TO_SEND_AUTH_TOKEN_IN_ALL_REQUEST_HEADERS")


class UserLogout(AppCreateAPIView):

    @require_loggedin_user
    def post(self, request):
        user = self.get_auth_data(request)
        if user:
            user.status = 0
            user.save()
            return self.send_response(message="Successfully logged out!")
        else:
            return self.send_error_response(message="Logged in user not founded!")


class SearchAPI(AppListAPIView):

    pagination_class = LOPagination

    @require_loggedin_user
    def get(self, request):
        search_val = self.request.GET["key"]
        try:
            user = User.objects.get(Q(email=search_val) | Q(name=search_val))
            serializer = common_serializer(User, meta_fields=["id", "name", "email"])(user)
            return self.send_response(data=serializer.data)
        except:
            user_set = User.objects.filter(Q(email__icontains=search_val) | Q(name__icontains=search_val))
            paginator = LOPagination()
            page =  paginator.paginate_queryset(user_set, request)
            serializer = common_serializer(User, meta_fields=["id", "name", "email"])(page, many=True)
            return paginator.get_paginated_response(serializer.data)