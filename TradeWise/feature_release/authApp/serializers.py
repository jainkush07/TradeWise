from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import UserDeviceTokens, UserAdvisors


#
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phoneNumber = serializers.CharField(required=False)
    countryCode = serializers.CharField(required=False)
    password = serializers.CharField(max_length=60, min_length=6)

    class Meta:
        model = User
        fields = ['id', 'usrname', 'password']


class CheckLoginCredentialSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['email']


#
class resetOrCreatePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=60, min_length=6)
    confirm_password = serializers.CharField(max_length=60, min_length=6)

    class Meta:
        model = User
        fields = ['password', 'confirm_password']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, min_length=6, max_length=68, write_only=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserDeviceTokensSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserDeviceTokens
        fields = "__all__"

class UserAdvisorSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAdvisors
        fields = "__all__"

