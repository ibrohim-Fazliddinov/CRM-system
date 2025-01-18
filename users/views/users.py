from crum import get_current_user
from django.contrib.auth import get_user_model
from djoser.serializers import ActivationSerializer
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from common.views import ExtendedUserViewSet
from users.serializers.api.serializer_user import (
    RegistrationsSerializer,
    UserSearchListSerializer,
    UserListSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer,
    CustomResetPasswordSerializer,
    CustomResetPasswordConfirmSerializer,
)

User = get_user_model()

@extend_schema_view(
    registration=extend_schema(
        summary='',
        tags=['Пользователь']
    ),
    activate=extend_schema(
        summary='',
        tags=['Пользователь']
    ),
    user_search=extend_schema(
        summary='',
        tags=['Пользователь']
    ),

    user_list=extend_schema(
        summary='',
        tags=['Пользователь']
    ),

    user_update=extend_schema(
        summary='',
        tags=['Пользователь']
    )
)
class AuthView(ExtendedUserViewSet):
    serializer_class = UserListSerializer()
    multi_serializer_class = {
        'registration': RegistrationsSerializer,
        'activate': ActivationSerializer,
        'user_search': UserSearchListSerializer,
        'user_list': UserListSerializer,
        'user_update': UserUpdateSerializer,
    }
    queryset = User.objects.all()

    @action(methods=['POST'], detail=False)
    def registration(self, request: Request, *args: None, **kwargs: None) -> Response:
        """Метод регистрации"""
        return self.create(request, *args, **kwargs)

    @action(methods=['POST'], detail=False)
    def activate(self, request: Request, *args: None, **kwargs: None) -> Response:
        pass

    @action(methods=['GET'], detail=False)
    def user_list(self, request: Request, *args: None, **kwargs: None) -> Response:
        pass

    @action(methods=['PUT', 'PATCH'], detail=False)
    def user_update(self, request: Request, *args: None, **kwargs: None) -> Response:
        pass

    @action(methods=['GET'], detail=False)
    def user_search(self, request: Request, *args: None, **kwargs: None) -> Response:
        pass



@extend_schema_view(
    change_password=extend_schema(
        summary='',
        tags=['Пароль'],
    ),

    reset_password=extend_schema(
        summary='',
        tags=['Пароль']
    ),

    reset_password_confirm=extend_schema(
        summary='',
        tags=['Пароль']
    )
)
class PasswordChangingView(ExtendedUserViewSet):

    serializer_class = ChangePasswordSerializer()
    multi_serializer_class = {
        'change_password': ChangePasswordSerializer,
        'reset_password': CustomResetPasswordSerializer,
        'reset_password_confirm': CustomResetPasswordConfirmSerializer
    }

    @action(methods=['POST'], detail=False)
    def change_password(self, request: Request) -> Response:
        user = get_current_user()
        serializer = self.get_serializer(instance=user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_204_NO_CONTENT)

    @action(methods=['POST'], detail=False)
    def reset_password(self, request: Request, *args: None, **kwargs: None) -> Response:
        pass

    @action(methods=['POST'], detail=False)
    def reset_password_confirm(self, request: Request, *args: None, **kwargs: None) -> Response:
        pass

