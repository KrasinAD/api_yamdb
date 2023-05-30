from django.contrib.auth import get_user_model
from django.db import models

# User = get_user_model()


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
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, related_name='titles')
    description = models.TextField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True, default=None)
    year = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='titles')

    def __str__(self):
        return self.description


class Review(models.Model):
    text = models.TextField()
    author = models.IntegerField()
    score = models.IntegerField(choices=[(i, i) for i in range(1, 11)])
    pub_date = models.DateTimeField(auto_now_add=True)
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='reviews')
#   author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='titles')

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.IntegerField()
    text = models.TextField()
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='comments')
#   author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='titles')
    
    def __str__(self):
        return self.text
