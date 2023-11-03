from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

ROLES = (
    ('admin', 'admin'),
    ('moderator', 'moderator'),
    ('user', 'user')
)


class User(AbstractUser):
    email = models.EmailField(max_length=254,
                              unique=True,
                              verbose_name='email')
    username = models.CharField(max_length=150,
                                unique=True,
                                validators=[RegexValidator
                                            (regex='^[a-zA-Z0-9_]+$')],
                                verbose_name='username')
    bio = models.CharField(max_length=300,
                           blank=True,
                           verbose_name='biography')
    role = models.CharField(choices=ROLES,
                            max_length=30,
                            blank=True,
                            default='user',
                            verbose_name='Role')
    confirmation_code = models.CharField(max_length=254,
                                         blank=True,
                                         null=True,
                                         verbose_name='confirmation_code')

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == 'moderator' or self.is_superuser

    @property
    def is_user(self):
        return self.role == 'user' or self.is_superuser
