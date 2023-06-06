from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

ROLES = (
    ('user', 'User'),
    ('moderator', 'Moderator'),
    ('admin', 'Admin'),
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
        max_length=20,
        choices=ROLES,
        default='user'
    )

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    def __str__(self):
        return self.username[:50]


class Category(models.Model):
    slug = models.SlugField(max_length=50, unique=True)
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Genre(models.Model):
    slug = models.SlugField(max_length=50, unique=True)
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True, default=None)
    year = models.IntegerField()
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles'
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='genres'
    )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)


class Review(models.Model):
    text = models.TextField()
    score = models.PositiveSmallIntegerField(
        default=None,
        validators=(MaxValueValidator(10, 'Оценка может быть от 1 до 10!'),
                    MinValueValidator(1, 'Оценка может быть от 1 до 10!'))
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name='reviews'
                              )
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='reviews')

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               related_name='comments')
    pub_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments')

    def __str__(self):
        return self.text
