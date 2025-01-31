from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from core.constants import (
    MAX_EMAIL_LENGTH,
    MAX_FIRST_NAME_LENGTH,
    MAX_LAST_NAME_LENGTH,
    MAX_USERNAME_LENGTH,
    USERNAME_REGEX
)


class User(AbstractUser):
    """Кастомная модель пользователя."""

    email = models.EmailField(
        max_length=MAX_EMAIL_LENGTH,
        unique=True,
        verbose_name='Адрес электронной почты',
    )
    username = models.CharField(
        max_length=MAX_USERNAME_LENGTH,
        unique=True,
        validators=(RegexValidator(USERNAME_REGEX),),
        verbose_name='Никнейм'
    )
    first_name = models.CharField(
        max_length=MAX_FIRST_NAME_LENGTH,
        verbose_name='Имя пользователя'
    )
    last_name = models.CharField(
        max_length=MAX_LAST_NAME_LENGTH,
        verbose_name='Фамилия пользователя'
    )
    avatar = models.ImageField(
        null=True,
        upload_to='users/avatars/',
        default=None,
        verbose_name='Аватар'
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
        'password'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    """Модель подписки. """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='followings',
        verbose_name='Пользователь'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author',
        verbose_name='Подписан на'
    )

    class Meta:
        ordering = ('user__username',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_user_author'
            ),
            models.CheckConstraint(
                name='check_user_author',
                check=~models.Q(user=models.F("author")),
            )
        ]

    def __str__(self):
        return (
            f'Пользователь: {self.user} '
            f'Подписан на: {self.author} '
        )
