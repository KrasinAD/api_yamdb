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
