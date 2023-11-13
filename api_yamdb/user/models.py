from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

ROLE_CHOICE = (
    ('admin', 'admin'),
    ('moderator', 'moderator'),
    ('user', 'user')
)
ADMIN = 'admin'
MODERATOR = 'moderator'


class User(AbstractUser):
    email = models.EmailField(max_length=254,
                              unique=True,
                              verbose_name='email')

    bio = models.CharField(max_length=300,
                           blank=True,
                           verbose_name='biography')
    role = models.CharField(choices=ROLE_CHOICE,
                            max_length=30,
                            blank=True,
                            default='user',
                            verbose_name='Role')

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == MODERATOR or self.is_staff
