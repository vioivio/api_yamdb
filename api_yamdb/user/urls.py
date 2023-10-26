from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, TokenView

router_v1 = DefaultRouter()
router_v1.register(r'v1/users', UserViewSet, basename='user')


urlpatterns = [
    path('', include(router_v1.urls)),
    path('v1/auth/token/', TokenView.as_view(), name='token')
]