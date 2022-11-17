from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate
import jwt
from termcolor import colored
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from datetime import timedelta
from .models import User
from django.conf import settings

# Not using
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        } 

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

# my token 
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # add custom claims
        token['username'] = user.email
        # print(token)
        return token



class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128, write_only=True,
        style={
            'input_type': 'password',
            'placeholder': 'Password'},
        required=True,
    )
    class Meta:
        model = User
        fields = (
            'email', 'password', 'username'
        )
    def create(self, validated_date):
        auth_user = User.objects.create_user(**validated_date)
        return auth_user


class UserLoginSerializer(serializers.Serializer):
    # email = serializers.EmailField()
    username = serializers.CharField(
        max_length=128
    )
    password = serializers.CharField(
        max_length=128, write_only=True
    )
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        username = data['username']
        password = data['password']
        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid login credential")

        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)

            update_last_login(None, user)

            validation = {
                'access': access_token,
                'refresh': refresh_token,
                'username': user.username,
            }

            return validation
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid login credential")


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
        )
        