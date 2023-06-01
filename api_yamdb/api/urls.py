from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from django.urls import include, path

from api.views import UserViewSet, UserAccessViewSet, UserCreateViewSet

app_name = 'api_yamdb'

router = DefaultRouter()
router.register(r'auth/signup/', UserCreateViewSet, basename='signup')
router.register(r'auth/token/', UserAccessViewSet, basename='token')
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router.urls)),
    # path('v1/auth/signup/', UserCreatViewSet, name='signup'),
    # path('v1/auth/token/', TokenObtainPairView.as_view(), name='token'),
    # path('v1/auth/signup/', include('djoser.urls')),
    # path('v1/', include('djoser.urls.jwt')),
]
