from django.core.mail import send_mail

from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .permissions import IsAuthorOrReadOnly
from .serializers import CommentSerializer, CategorySerializer, GenreSerializer, ReviewSerializer, TitleSerializer 
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




class ConfirmEmailViewSet(viewsets.ViewSet):
    def create(self, request):
        email = request.data.get('email')
        if email:
            # Генерация случайного кода подтверждения
            confirmation_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            # Отправка кода по электронной почте
            send_mail(
                'Код подтверждения',
                f'Ваш код подтверждения: {confirmation_code}',
                'from@example.com',
                [email],
                fail_silently=False
            )
            # Возвращаем сообщение об успешной отправке
            return Response({'message': 'Код подтверждения отправлен'})
        else:
            # Возвращаем сообщение об ошибке, если email не указан
            return Response({'message': 'Не указан email'}, status=400)

