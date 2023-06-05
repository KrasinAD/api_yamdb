from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from reviews.models import CustomUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import action
from django.contrib.auth.tokens import default_token_generator

from .permissions import IsAuthorOrReadOnly
from .serializers import (CommentSerializer,
                          CustomUserSerializer,
                          CategorySerializer,
                          GenreSerializer,
                          ReviewSerializer,
                          TitleSerializer,
                          TokenObtainPairByEmailSerializer
) 
from reviews.models import Category, Genre, Title, Review


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

#    def perform_create(self, serializer):
#       serializer.save(author=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    serializer_class = GenreSerializer
    permission_classes = (IsAuthorOrReadOnly,)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        return Review.objects.filter(title=title_id)

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = Review.objects.get(pk=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = Review.objects.select_related('comments').filter(
            title=title_id).get(pk=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = Review.objects.select_related('comments').filter(
            title=title_id).get(pk=review_id)
        serializer.save(author=self.request.user, review=review)


class SignupView(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        if not username or not email:
            return Response({'error': 'username и email нужны!'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            user = CustomUser.objects.create(
                username=username,
                email=email,
                is_active=False,
            )
        except Exception as e:
            return Response({'error': str(e)},
                             status=status.HTTP_400_BAD_REQUEST
                            )
        
        confimation_code = default_token_generator.make_token(user)

        send_mail(
            'Код подтверждения',
            f'Ваш код подтверждения: {confimation_code}',
            'ounap2010@yandex.ru',
            [email],
            fail_silently=False,
        )

        return Response({'success': 'код подтверждения был отправлен на ваш эл.адрес'})
    

class TokenObtainPairByEmailView(TokenObtainPairView):
    serializer_class = TokenObtainPairByEmailSerializer
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        confirmation_code = request.data.get('confirmation_code')
        
        if not email or not confirmation_code:
            return Response({'error': 'нужны email и код подтверждения'})
        
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'почта не существует'},
                             status=status.HTTP_400_BAD_REQUEST)
        
        if confirmation_code != '328593':
            return Response({'error': 'неверный код подтверждения'},
                             status=status.HTTP_400_BAD_REQUEST)
        

        response = super().post(request, *args, **kwargs)
        tokens = user.get_tokens()
        response.data.update(tokens)
        return response


class CustomUserViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthenticated,)
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'

    @action(methods=['GET', 'PATCH'],
        detail=False,
        url_path='me',
        permission_classes= [AllowAny]
    )
    def me(self, request):
        user = get_object_or_404(CustomUser, username=self.request.user)
        if request.method == 'PATCH':
            serializer = CustomUserSerializer(
                user,
                data=request.data,
                context ={'request': request}
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save(role='user')
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=400)
        serializer = self.get_serializer(user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)from django.contrib.auth.tokens import default_token_generator
from rest_framework import mixins, status, viewsets 
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import (UserCreateSerializer, UserSerializer,
                          UserTokenSerializer)
from reviews.models import User


class UserCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Вьюсет для создания пользователя User."""
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, _ = User.objects.get_or_create(**serializer.validated_data)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Подтверждение регистрации.',
            f'Направляем код подтверждения: {confirmation_code}',
            'admin@yamdb.com', 
            [user.email], 
            fail_silently=False,
        ) 
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserTokenViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Вьюсет для обработки JWT-токена."""
    queryset = User.objects.all()
    serializer_class = UserTokenSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = UserTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = get_object_or_404(User, username=username)

        if not default_token_generator.check_token(user, confirmation_code):
            message = {'confirmation_code': 'Код подтверждения не верный.'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        message = {'token': str(AccessToken.for_user(user))}
        return Response(message, status=status.HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для взаимодействия с пользователем."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = (IsAdminUser,)

    # def perform_create(self, serializer):
    #     serializer.save(username=self.request.user)




