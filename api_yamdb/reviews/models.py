from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

CHOICES_ROLES = (
    ('user', 'User'),
    ('moderator', 'Moderator'),
    ('admin', 'Admin'),
)


class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=20,
                            choices=CHOICES_ROLES,
                            default='user')
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = ['email']

    @property
    def is_staff(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'


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
    author = models.IntegerField()
    score = models.PositiveSmallIntegerField(
        default=None,
        validators=(MaxValueValidator(10), MinValueValidator(1))
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name='reviews'
                              )
    author = models.ForeignKey(CustomUser,
                               on_delete=models.CASCADE,
                               related_name='reviews'
                               )

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               related_name='comments')
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.IntegerField()
    text = models.TextField()
    author = models.ForeignKey(CustomUser,
                               on_delete=models.CASCADE,
                               related_name='comments'
                               )

    def __str__(self):
        return self.text
