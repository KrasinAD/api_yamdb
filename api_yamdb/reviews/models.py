from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework_simplejwt.tokens import RefreshToken

CHOICES_ROLES = [
    ('user', 'User'),
    ('moderator', 'Moderator'),
    ('admin', 'Admin'),
]


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('У пользователя email - musthave')
        
        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        if password:
            user.set_password(password)

        user.save()
        return user
    
    def create_superuser(self, username, email, password):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.is_superuser = True
        user.save()
        return user

class CustomUser(AbstractBaseUser):
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=20,
                            choices=CHOICES_ROLES,
                            default='user'
                            )

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return True
    
    @property
    def is_staff(self):
        return self.role == 'admin'
    
    def get_tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


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
        return self.description

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
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='reviews'
                               )

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               related_name='comments'
                               )
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.IntegerField()
    text = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name='comments'
                               )

    def __str__(self):
        return self.text
