from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator
from rest_framework.response import Response

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User
from users.utils import send_confirmation_code


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class UserCreateSerializer(serializers.Serializer):
    # username = serializers.RegexField(
    #     regex=r'^[\w.@+-]+$',
    #     max_length=150,
    # )
    # email = serializers.EmailField(
    #     max_length=254,
    # )

    # def validate(self, data):
    #     username = User.objects.filter(username=data['username'])
    #     email = User.objects.filter(email=data['email'])
    #     if data.get('username') == 'me':
    #         raise serializers.ValidationError(
    #             'Использовать имя me запрещено'
    #         )
    #     if username and not email:
    #         raise serializers.ValidationError(
    #             'Пользователь с таким username уже существует'
    #         )
    #     if email and not username:
    #         raise serializers.ValidationError(
    #             'Пользователь с таким email уже существует'
    #         )
    #     return data

    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    email = serializers.EmailField(
        max_length=254,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    def validate_username(self, value):
        if value == "me":
            raise serializers.ValidationError('Использовать имя me запрещено')
        return value

    class Meta:
        fields = ("username", "email")
        model = User

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        send_confirmation_code(
            email=email,
            confirmation_code=default_token_generator.make_token(username)
        )
        return Response(validated_data)


class UserTokenSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )
    confirmation_code = serializers.CharField(
        max_length=150,
        required=True
    )

    def validate(self, data):
        username = data['username']
        confirmation_code = data['confirmation_code']
        user = get_object_or_404(User, username=username)
        if not default_token_generator.check_token(user, confirmation_code):
            raise serializers.ValidationError(
                '{confirmation_code}: Код подтверждения не верный.'
            )


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('slug', 'name')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('slug', 'name')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField(read_only=True)
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )

    def get_rating(self, obj):
        return obj.reviews.all().aggregate(Avg('score'))['score__avg']


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError('Нельзя одному автору оставлять больше '
                                      'одного отзыва на одно произведение')
        return data
