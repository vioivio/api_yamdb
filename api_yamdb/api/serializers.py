from django.contrib.auth.tokens import default_token_generator
from django.core.validators import RegexValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title
from user.models import User
from datetime import timezone


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=256)
    username = serializers.CharField(max_length=150,
                                     validators=[RegexValidator(
                                          regex='^[a-zA-Z0-9_]+$')])

    def validate(self, attrs):
        if (not User.objects.filter(username=attrs['username']).exists() and
           User.objects.filter(email=attrs['email']).exists()):
            raise serializers.ValidationError({"Signup error":
                                               "Email занят"})

        elif (User.objects.filter(username=attrs['username']).exists() and
              not User.objects.filter(email=attrs['email']).exists()):
            raise serializers.ValidationError({"Signup error":
                                               "Username занят"})
        if attrs['username'] == 'me':
            raise serializers.ValidationError(
                {"Signup error": "Недоступный username"}
            )
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role')
        model = User

    def validate_role(self, attrs):
        user = self.context['request'].user
        if user.role != 'admin' and user.role != attrs:
            raise serializers.ValidationError("You can not change the role")
        return super().validate(attrs)


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if not default_token_generator.check_token(user,
                                                   data['confirmation_code']):
            raise serializers.ValidationError(
                {'confirmation_code': 'Invalid verification code'})
        return data


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


class TitleCreateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        read_only=False,
        queryset=Genre.objects.all(),
        slug_field='slug'
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'

    def validate_date(value):
        now = timezone.now().year
        if value > now:
            raise serializers.ValidationError(
                f'{value} не может быть больше {now}'
            )


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

    def validate_score(self, value):
        if 1 > value > 10:
            raise serializers.ValidationError(
                'Оценка может быть от 1 до 10'
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
