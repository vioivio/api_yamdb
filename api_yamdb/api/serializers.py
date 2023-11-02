from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title
from user.models import User


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()

    def validate(self, attrs):
        if attrs['username'] == 'me':
            raise serializers.ValidationError(
                {"Signup error": "Недоступный username"}
            )
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        model = User


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, attrs):
        if not User.objects.filter(username=attrs['username'],
                                   confirmation_code=attrs['confirmation_code']):
            raise serializers.ValidationError({"auth_errors":"Неверные данные авторизации"})
        return attrs


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ['id']
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ['id']
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.FloatField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    score = serializers.IntegerField()
    title = serializers.PrimaryKeyRelatedField(read_only=True)

    def validate(self, value):
        author = self.context['request'].user
        title_id = (self.context['request'].
                    parser_context['kwargs'].get('title_id'))
        title = get_object_or_404(
            Title,
            id=title_id
        )
        if (self.context['request'].method == 'POST'
                and title.reviews.filter(author=author).exists()):
            raise serializers.ValidationError(
                f'Отзыв на произведение {title.name} уже существует'
            )
        return value

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    review = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment
