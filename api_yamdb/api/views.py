from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, views, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Category, Genre, Review, Title
from user.models import User
from .filters import TitleFilter

from .permissions import (AdminOrReadOnly,
                          OnlyAdminPermission,
                          PrivilegeOrReadOnly,
                          UserProfilePermission,
                          )
from .serializers import (CategorySerializer,
                          CommentSerializer,
                          GenreSerializer,
                          ReviewSerializer,
                          SignUpSerializer,
                          TitleSerializer,
                          TokenSerializer,
                          UserSerializer,
                          TitleCreateSerializer,
                          )


class SignUpCreate(views.APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        username = serializer.data.get('username')
        user, code = User.objects.get_or_create(email=email, username=username)
        confirmation_code = default_token_generator.make_token(user)
        user.confirmation_code = confirmation_code
        user.save()
        send_mail(
            subject='Confirmation_code',
            message=f"Code: {confirmation_code}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated,
                          OnlyAdminPermission | UserProfilePermission]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_url_kwarg = 'username'
    lookup_field = 'username'

    def get_object(self):
        if self.kwargs['username'] == 'me':
            user = self.request.user
            self.check_object_permissions(self.request, user)
            return user
        return super().get_object()

    def destroy(self, request, *args, **kwargs):
        if self.kwargs['username'] == 'me':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT' and self.kwargs['username'] != 'me':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)


class TokenView(views.APIView):
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        confirmation_code = serializer.data.get('confirmation_code')
        user = get_object_or_404(User, username=username,
                                 confirmation_code=confirmation_code)
        token = RefreshToken.for_user(user)
        return Response({'token': str(token.access_token)},
                        status=status.HTTP_200_OK)


class CategoryViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


# class TitleViewSet(viewsets.ModelViewSet):
#     queryset = Title.objects.all().order_by('name')
#     serializer_class = TitleSerializer
#     permission_classes = (AdminOrReadOnly,)
#     http_method_names = ['get', 'post', 'patch', 'delete', 'create']


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().order_by('name')
    serializer_class = TitleSerializer
    permission_classes = (AdminOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete', 'create']
    create_serializer_class = TitleCreateSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PATCH':
            return self.create_serializer_class
        return super().get_serializer_class()

    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

        return super().update(request, *args, **kwargs)


class GenreViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    http_method_names = ['get', 'post', 'patch', 'delete', 'create']


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (PrivilegeOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete', 'create']

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (PrivilegeOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete', 'create']

    def get_queryset(self):
        review = get_object_or_404(
            Review, id=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
