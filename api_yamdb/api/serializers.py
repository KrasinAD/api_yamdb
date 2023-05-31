from rest_framework import serializers
# from rest_framework.relations import SlugRelatedField
from django.db.models import Avg

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from datetime import timezone


class YearValidator:
    def __call__(self, value):
        if value < 1900 or value > timezone.now().year:
            raise serializers.ValidationError('Invalid Year')

class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    year = serializers.IntegerField(validators=[YearValidator()])

    class Meta:
        fields = '__all__'
        model = Title

    def get_rating(self, obj):
        return obj.reviews.all().aggregate(Avg('score'))['score__avg']


class CommentSerializer(serializers.ModelSerializer):
    # author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    # author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'score,' 'pub_date')
        model = Review


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugRelatedField(required=True)
    name = serializers.CharField(required=True)

    class Meta:
        fields = ('slug', 'name')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    slug = serializers.SlugRelatedField(required=True)
    name = serializers.CharField(required=True)

    class Meta:
        fields = ('slug','name')
        model = Genre


class GenreTitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer()
    title = TitleSerializer()
    titles = serializers.ManyRelatedField(TitleSerializer)

    class Meta:
        fields = ('genre', 'title', 'titles')
        model = GenreTitle
