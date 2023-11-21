from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator

from .constants import (EMAIL_LENGTH,
                        USERNAME_LENGTH,
                        BIO_LENGTH,
                        ROLE_LENGTH)
from .validators import validate_me

ADMIN = 'admin'
MODERATOR = 'moderator'
USER = 'user'

ROLE_CHOICE = (
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
    (USER, USER))


class User(AbstractUser):
    email = models.EmailField(max_length=EMAIL_LENGTH,
                              unique=True,
                              verbose_name='email')

    username = models.CharField(max_length=USERNAME_LENGTH,
                                unique=True,
                                validators=[UnicodeUsernameValidator(),
                                            validate_me])

    bio = models.CharField(max_length=BIO_LENGTH,
                           blank=True,
                           verbose_name='biography')
    role = models.CharField(choices=ROLE_CHOICE,
                            max_length=ROLE_LENGTH,
                            blank=True,
                            default='user',
                            verbose_name='Role')

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == MODERATOR or self.is_staff
