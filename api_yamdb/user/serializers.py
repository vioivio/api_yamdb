from typing import Any, Dict
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = CustomUser


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    #confirmation code(ind)