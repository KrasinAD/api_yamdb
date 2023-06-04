from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny, IsAdminUser

from .serializers import (UserAccessSerializer, UserCreateSerializer, 
                          UserSerializer)
from review.models import User


class UserCreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Вьюсет для создания пользователя User."""
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)

    # def create(self, request):
    #     pass


class UserAccessViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """Вьюсет для обработки JWT-токена."""
    queryset = User.objects.all()
    serializer_class = UserAccessSerializer
    permission_classes = (AllowAny,)

    # def create(self, request):
    #     pass

class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для взаимодействия с пользователем."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = (IsAdminUser,)

    # def perform_create(self, serializer):
    #     serializer.save(username=self.request.user)




