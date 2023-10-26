from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import (RegexValidator)


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