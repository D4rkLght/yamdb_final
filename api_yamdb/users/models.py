from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    ROLES = (
        (ADMIN, 'Administrator'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=True,
    )
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        unique=True,
        max_length=254
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=254,
        choices=ROLES,
        default=USER
    )
    bio = models.TextField(
        verbose_name='О себе',
        null=True,
        blank=True
    )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser or self.is_staff

    @property
    def is_user(self):
        return self.role == self.USER

    class Meta:
        ordering = ('id', )
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
