from rest_framework import serializers, validators
from django.core.validators import MaxLengthValidator
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

class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField(
        validators=[
            validators.UniqueValidator(queryset=CustomUser.objects.all()),
            MaxLengthValidator(254),
        ]
    )

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email']
        )
        return user


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

    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        return token