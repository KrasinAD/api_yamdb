from rest_framework import serializers
# from rest_framework.relations import SlugRelatedField
from django.db.models import Avg

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from datetime import timezone


class YearValidator:
    def __call__(self, value):
        if value < 1900 or value > timezone.now().year:
            raise serializers.ValidationError('Invalid Year')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('slug', 'name')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    year = serializers.IntegerField(validators=[YearValidator()])
    genre = GenreSerializer(many=True)

    class Meta:
        fields = '__all__'
        model = Title

    def get_rating(self, obj):
        return obj.reviews.all().aggregate(Avg('score'))['score__avg']
  
    def create(self, validated_data):
        if 'genre' not in self.initial_data:
            title = Title.objects.create(**validated_data)
            return title
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        for genre in genres:
            current_genre, status = Genre.objects.get_or_create(**genre)
            GenreTitle.objects.create(genre=current_genre, title=title)
        return title


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

    class Meta:
        fields = ('slug', 'name')
        model = Category
