from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = CustomUser


class TokenSerializer(serializers.Serializer):
    # Использвуется username и confirmation code для получ

    username = serializers.CharField()
    # confirmation code(ind)