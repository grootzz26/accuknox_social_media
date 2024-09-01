from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from django.apps import apps as manager
from apps.user_app.models import User, Token


class AppViewMixin:

    def get_valid_serializer(self, serializer_class=None):
        """Central function to get the valid serializer. Raises exceptions."""
        assert self.serializer_class or serializer_class

        if not serializer_class:
            serializer_class = self.serializer_class
        serializer = serializer_class(
            data=self.request.data, context={"request": self.request}
        )
        serializer.is_valid(raise_exception=True)
        return serializer


    def send_error_response(self, data=[], message="", status=status.HTTP_400_BAD_REQUEST):
        return self.send_response(data=data, message=message, status_code=status)

    @staticmethod
    def send_response(data=[], message="", status_code=status.HTTP_200_OK, action_code=None, **other):
        return Response(
            data={
                "data": data,
                "message": message,
                "status": "success" if status.is_success(status_code) else "error",
                "action_code": action_code if action_code else "DO_NOTHING",  # make the FE do things based on this
                **other,
            },
            status=status_code,
        )

    @staticmethod
    def get_object_or_none(model=None, **data):
        model = manager.get_model(app_label=model[-1], model_name=model[0])
        try:
            return model.object.get(**data)
        except:
            return None

    def get_user(self):
        try:
            return User.objects.get(**self.request.data)
        except:
            return None

    @staticmethod
    def get_auth_data(request):
        try:
            token = request.META["HTTP_AUTHORIZATION"]
            return Token.objects.get(token=token)
        except:
            return None


class AppCreateAPIView(AppViewMixin, CreateAPIView):
    pass

class AppListAPIView(AppViewMixin, ListAPIView):
    pass

def require_loggedin_user(view_func):

    def decorators(*args, **kwargs):
        request = args[-1]
        resp = AppViewMixin()
        try:
            auth_token = request.META.get("HTTP_AUTHORIZATION", False)
        except AttributeError:
            return resp.send_error_response(data="CHECK_HEADER", status=status.HTTP_400_BAD_REQUEST)
        if auth_token:
            try:
                auth_data = resp.get_auth_data(request)
                if auth_data.status:
                    return view_func(*args, **kwargs)
                else:
                    return resp.send_error_response(data="Non Logged In User!", status=status.HTTP_400_BAD_REQUEST)
            except:
                return resp.send_error_response(data="INVALID_AUTH_TOKEN", status=status.HTTP_401_UNAUTHORIZED)
        else:
            return resp.send_error_response(data="INVALID_AUTH_TOKEN", status=status.HTTP_401_UNAUTHORIZED)

    return decorators
