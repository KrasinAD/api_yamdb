from django.db import models
from django.contrib.auth.models import AbstractUser


CHOICES_ROLE = (
    ('User', 'Пользователь'),
    ('Moderator', 'Модератор'),
    ('Admin', 'Администратор'),
)

class CustomUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    role = models.CharField(max_length=16, choices=CHOICES_ROLE)