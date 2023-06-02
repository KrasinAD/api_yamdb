# from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from reviews.models import CustomUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .permissions import IsAuthorOrReadOnly
from .serializers import (CommentSerializer,
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
        
        confimation_code = '328593'

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
