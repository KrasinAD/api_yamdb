from rest_framework.routers import DefaultRouter

from django.urls import include, path

from api.views import UserCreateViewSet, UserTokenViewSet, UserViewSet

app_name = 'api_yamdb'

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/auth/signup/',
         UserCreateViewSet.as_view({'post': 'create'}), name='signup'),
    path('v1/auth/token/',
         UserTokenViewSet.as_view({'post': 'create'}), name='token'),
    path('v1/', include(router.urls)),
]
