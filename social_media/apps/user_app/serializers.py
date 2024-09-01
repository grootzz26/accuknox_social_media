from rest_framework import serializers
from .models import User, Token
from apps.common.helpers import generate_auth_token


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("name", "email", "password",)

    def validate(self, value):
        if any(char.isdigit() for char in value["name"]):
            raise serializers.ValidationError('Name should contain characters only.')
        if 8 <= len(value["password"]) > 3:
            raise serializers.ValidationError('password shoud be in range between 4 and 8 letters.')
        return value


class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, value):
        try:
            user = User.objects.get(email=value["email"])
        except:
            raise serializers.ValidationError("User doesn't exists!. Do sign up")
        if value['password'] != user.password:
            raise serializers.ValidationError("Incorrect password!")
        return user
