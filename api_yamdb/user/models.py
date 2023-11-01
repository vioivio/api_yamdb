from django.db import models
from django.contrib.auth.models import AbstractUser


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
                                verbose_name='username')
    bio = models.CharField(max_length=300,
                           blank=True,
                           verbose_name='biography')
    role = models.CharField(choices=ROLES,
                            max_length=10,
                            blank=True,
                            default='user',
                            verbose_name='Role')

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_user(self):
        return self.role == 'user'
