from django.db import models
from django.contrib.auth.models import AbstractUser


ROLE = (
    ('User', 'Пользователь'),
    ('Moderator', 'Модератор'),
    ('Admin', 'Администратор'),
)

class User(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(
        'Биография',
        max_length=500,
        blank=True
    )
    role = models.CharField(
        'Тип пользователя',
        max_length=16,
        choices=ROLE,
        default='User'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username[:50]