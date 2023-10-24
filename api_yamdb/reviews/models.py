from django.contrib.auth.models import AbstractUser
from django.core.validators import (MaxValueValidator, MinValueValidator, RegexValidator)
from django.db import models

from .validators import validate_date

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

ROLES_CHOICES = [
    (USER, USER),
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
]


class User(AbstractUser):
    """Модель пользователя"""
    username = models.CharField(
        'Имя пользователя',
        max_length=100,
        unique=True,
        blank=False,
        null=False,
        validators=[RegexValidator(
            regex='^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$'
        )
        ]
    )
    email = models.EmailField(
        'Адрес e-mail',
        max_length=254,
        unique=True,
        blank=False,
        null=False
    )
    role = models.CharField(
        'Роль',
        max_length=20,
        choices=ROLES_CHOICES,
        default=USER,
        blank=True
    )
    bio = models.TextField(
        'Описание профиля',
        blank=True,
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True
    )

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'

    def __str__(self):
        return self.username


class Category(models.Model):
    """Модель категории"""
    name = models.CharField('Название категории', max_length=256)
    slug = models.SlugField(
        unique=True,
        max_length=50,
        validators=[RegexValidator(regex='^[a-zA-Z0-9_]+$')]
    )

    class Meta:
        verbose_name = 'Категория'

    def __str__ (self):
        return self.slug


class Genre(models.Model):
    """Модель жанров"""
    name = models.CharField(
        'Жанр',
        max_length=200
    )
    slug = models.SlugField(
        unique=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Жанр'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений"""
    name = models.CharField(
        'Название произведения',
        max_length=200,
        db_index=True
    )
    year = models.IntegerField(
        'Год выпуска',
        validators=(validate_date,)
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
        blank=True
    )
    description = models.TextField(
        'Описание произведения',
        max_length=255,
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
    )

    class Meta:
        verbose_name = 'Произведение'

    def __str__(self):
        return self.name


class Review(models.Model):
    """Оценка произведения"""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.CharField(
        max_length=200
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.IntegerField(
        'Оценка',
        validators=(
            MinValueValidator(1),
            MaxValueValidator(10)
        ),
        error_messages={'validators': 'Оценка должна быть в диапазоне 1-10'}
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        verbose_name = 'Отзыв'
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author', ),
                name='review',
            )]
        ordering = ('pub_date',)

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель коммнтариев"""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.CharField(
        'Тело комментария',
        max_length=200
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'

    def __str__(self):
        return self.text
