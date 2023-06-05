from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from django.urls import include, path

from api.views import UserCreateViewSet, UserTokenViewSet, UserViewSet

app_name = 'api_yamdb'

router = DefaultRouter()
# router.register(r'auth/signup/', UserCreateViewSet, basename='signup')
# router.register(r'auth/token/', UserAccessViewSet, basename='token')
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/auth/signup/', UserCreateViewSet.as_view({'post': 'create'}), name='signup'),
    path('v1/auth/token/', UserTokenViewSet.as_view({'post': 'create'}), name='token'),
    path('v1/', include(router.urls)),
    # path('v1/auth/signup/', include('djoser.urls')),
    # path('v1/', include('djoser.urls.jwt')),
from rest_framework_simplejwt.views import TokenObtainPairView
from django.urls import include, path
from django import views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from .views import CategoryViewSet, CommentViewSet, GenreViewSet, ReviewViewSet, SignupView, TitleViewSet, TokenObtainPairByEmailView

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(
    'titles',
    TitleViewSet,
    basename='titles'
)
router_v1.register(
    'genres',
    GenreViewSet,
    basename='genres'
)
router_v1.register(
    'categories',
    CategoryViewSet,
    basename='categories'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('api/v1/auth/signup/', views.SignupView.as_view(), name="signup"),
    path('api/v1/auth/token/', TokenObtainPairByEmailView),
    path('v1/api-token-auth/', obtain_auth_token),
    path('v1/', include(router_v1.urls)),
]
