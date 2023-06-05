from rest_framework import serializers, validators
# from rest_framework.relations import SlugRelatedField
from django.db.models import Avg
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title, CustomUser
from datetime import timezone


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'bio',
            'role',
        )


class SignUpSerializer(serializers.Serializer):
    username = serializers.SlugField(max_length=150)
    email = serializers.EmailField(max_length=254)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email')

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Это имя уже занято'
            )
        if data['email'] == data['username']:
            raise serializers.ValidationError(
                'Поля не должны совпадать'
            )
        if CustomUser.objects.filter(email=data['email']):
            raise serializers.ValidationError(
                'Эта почта занята'
            )
        if (CustomUser.objects.filter(username=data['username'])
            and not CustomUser.objects.filter(email=data['email'])):
            raise serializers.ValidationError(
                'Пользователь зарегистрирован с другой почтой'
            )
        return data


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


class TokenObtainPairByEmailSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    confirmation_code = serializers.CharField()

    def validate(self, attrs):
        data = super().validate(attrs)
        email = attrs.get('email')
        confirmation_code = attrs.get('confirmation_code')

        if email and confirmation_code:
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError('Неверный email или код подтверждения')
            
            if not user.check_confirmation_code(confirmation_code):
                raise serializers.ValidationError('Неверный email или код подтверждения')
            data['user'] = user
        else:
            raise serializers.ValidationError('Email и код подтверждения обязательны')
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token
    

from rest_framework import serializers
from django.db import models

from reviews.models import User


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Использовать имя me запрещено'
            )
        if User.objects.filter(username=data.get('username')):
            raise serializers.ValidationError(
                'Пользователь с таким username уже существует'
            )
        if User.objects.filter(email=data.get('email')):
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует'
            )
        return data


class UserTokenSerializer(serializers.Serializer):

    # username = models.CharField(
    #     max_length=150,
    #     unique=True,
    # ),

    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )

    confirmation_code = serializers.CharField(
        max_length=150,
        required=True
    )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )