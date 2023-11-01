from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views


yamdb_v1_router = DefaultRouter()

# yamdb_v1_router.register(
#     'auth/signup',
#     views.SignUpCreate,
#     basename='signup'
# )
yamdb_v1_router.register(
    r'categories',
    views.CategoryViewSet,
    basename='categories'
)
yamdb_v1_router.register(
    r'genres',
    views.GenreViewSet,
    basename='genres'
)
yamdb_v1_router.register(
    r'titles',
    views.TitleViewSet,
    basename='titles'
)
yamdb_v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='reviews'
)
yamdb_v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
    r'/comments',
    views.CommentViewSet,
    basename='comments'
)
yamdb_v1_router.register(
    'users',
    views.UserViewSet,
    basename='profile'
)

urlpatterns = [
    path('v1/auth/token/', views.TokenView, name='token'),
    path('v1/', include(yamdb_v1_router.urls)),
]