from rest_framework import serializers
# from rest_framework.relations import SlugRelatedField
from django.db.models import Avg

from reviews.models import Comment, Review, Title


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Title

    def get_rating(self, obj):
        return obj.reviews.all().aggregate(Avg('score'))['score__avg']


class CommentSerializer(serializers.ModelSerializer):
    # author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'pubdate')
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    # author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'score,' 'pubdate')
        model = Review
