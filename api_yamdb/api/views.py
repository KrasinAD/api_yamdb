from django.contrib.auth.tokens import default_token_generator
from rest_framework import mixins, status, viewsets 
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.pagination import PageNumberPagination

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
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination

    # def perform_create(self, serializer):
    #     serializer.save(username=self.request.user)




