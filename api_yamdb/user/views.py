from django.shortcuts import get_object_or_404
from rest_framework import viewsets, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer, TokenSerializer
from .models import CustomUser
from .permissions import UserProfilePermission


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, UserProfilePermission]
    lookup_url_kwarg = 'username'
    lookup_field = 'username'

    def get_object(self):
        if self.kwargs['username'] == 'me':
            return self.request.user
        return super().get_object()


class TokenView(views.APIView):
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        user = get_object_or_404(CustomUser, username=username)
        # confirmation_code (in developing)
        token = RefreshToken.for_user(user)

        # Сделать правильный статус

        return Response({'token': str(token.access_token)}, status=200)
