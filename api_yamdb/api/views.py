from rest_framework import viewsets

from .serializers import UserSerializer
from review.models import CustomUser


class UserCreateViewSet(viewsets.ModelViewSet):
    """Вьюсет для создания пользователя User."""
    pass

class UserAccessViewSet(viewsets.ModelViewSet):
    """Вьюсет для обработки JWT-токена."""
    pass

class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для взаимодействия с пользователем."""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer



