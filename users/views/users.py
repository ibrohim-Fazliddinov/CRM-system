from crum import get_current_user
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
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
from rest_framework.filters import SearchFilter, OrderingFilter
User = get_user_model()


@extend_schema_view(
    registration=extend_schema(
        summary='Регистрация нового пользователя.',
        tags=['Пользователь']
    ),
    activate=extend_schema(
        summary='Активация учетной записи пользователя.',
        tags=['Пользователь']
    ),
    user_search=extend_schema(
        summary='Поиск пользователей по заданным фильтрам.',
        tags=['Пользователь']
    ),
    user_list=extend_schema(
        summary='Получение списка пользователей.',
        tags=['Пользователь']
    ),
    user_update=extend_schema(
        summary='Обновление данных пользователя.',
        tags=['Пользователь']
    )
)
class AuthView(ExtendedUserViewSet):
    """
    Класс представления для управления пользователями, включая регистрацию, активацию, поиск, получение списка и обновление данных пользователя.

    Используются сериализаторы для различных операций с пользователями, а также фильтры для поиска и сортировки.

    Методы:
    - registration: Метод для регистрации нового пользователя.
    - activate: Метод для активации учетной записи пользователя.
    - user_list: Метод для получения списка пользователей.
    - user_update: Метод для обновления данных пользователя.
    - user_search: Метод для поиска пользователей по заданным фильтрам и сортировке.
    """

    serializer_class = UserListSerializer()
    multi_serializer_class = {
        'registration': RegistrationsSerializer,
        'activate': ActivationSerializer,
        'user_search': UserSearchListSerializer,
        'user_list': UserListSerializer,
        'user_update': UserUpdateSerializer,
    }
    queryset = User.objects.all()

    def get_object(self) -> User:
        """
        Метод получения текущего пользователя.

        Используется для того, чтобы получить данные текущего пользователя на основе запроса.
        Это необходимо, чтобы избежать ошибок связанные с неопределенностью контекста в случае аутентифицированных пользователей.

        Возвращает:
            User: текущий пользователь, полученный из `request.user`.
        """
        return self.request.user
        # В этом методе мы явно указываем, что возвращаем текущего пользователя с помощью `self.request.user`,
        # что исключает ошибку "look_up fields". Эта ошибка может возникать, когда нет четко определенного
        # объекта, который можно использовать для идентификации записи в базе данных. В данном случае
        # мы уверены, что пользователь аутентифицирован, и объект `request.user` всегда доступен.

    @action(methods=['POST'], detail=False)
    def registration(self, request: Request, *args: None, **kwargs: None) -> Response:
        """
        Метод регистрации нового пользователя.

        Использует сериализатор для регистрации нового пользователя и вызывает стандартную операцию создания.

        Параметры:
            request: объект запроса, содержащий данные для регистрации.

        Возвращает:
            Response: Ответ с результатом регистрации.
        """
        return self.create(request, *args, **kwargs)

    @action(methods=['POST'], detail=False)
    def activate(self, request: Request, *args: None, **kwargs: None) -> Response:
        """
        Метод активации учетной записи пользователя.

        В данный момент не реализован, но должен быть использован для активации
        пользователя по какой-либо информации, например, через код активации.

        Параметры:
            request: объект запроса, содержащий данные для активации.

        Возвращает:
            Response: Ответ после выполнения активации.
        """
        pass

    @action(methods=['GET'], detail=False)
    def user_list(self, request: Request, *args: None, **kwargs: None) -> Response:
        """
        Метод для получения списка пользователей.

        В этом методе используется стандартный метод retrieve для получения списка всех пользователей.

        Параметры:
            request: объект запроса, может содержать параметры фильтрации, если они будут использованы.

        Возвращает:
            Response: Сериализованный список пользователей.
        """
        return self.retrieve(request, *args, **kwargs)

    @action(methods=['PUT', 'PATCH'], detail=False)
    def user_update(self, request: Request, *args: None, **kwargs: None) -> Response:
        """
        Метод для обновления данных пользователя.

        В зависимости от типа запроса (PUT или PATCH) выполняется полное обновление данных или частичное.
        Для этого используется словарь `update_methods`, который связывает методы с соответствующими действиями.

        Параметры:
            request: объект запроса, содержащий обновленные данные пользователя.

        Возвращает:
            Response: Ответ с результатами обновления.
        """
        update_methods = {'PUT': self.update, 'PATCH': self.partial_update}
        for method, func in update_methods.items():
            if method == request.method:
                return func(request, *args, **kwargs)

    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)  # Указываем фильтры
    search_fields = ('id', 'username', 'first_name', 'last_name', 'email')  # Параметры для поиска
    ordering_fields = ['username', 'id']  # Разрешённые поля для сортировки
    ordering = ['username', '-id']  # Сортировка по умолчанию

    @action(methods=['GET'], detail=False)
    def user_search(self, request: Request) -> Response:
        """
        Метод для поиска пользователей с применением фильтров и сортировки.

        В этом методе данные фильтруются в соответствии с параметрами запроса, после чего
        возвращается результат в виде списка пользователей.

        Параметры:
            request: объект запроса, содержащий параметры для фильтрации, поиска и сортировки.

        Возвращает:
            Response: Сериализованный список найденных пользователей.
        """
        queryset = self.filter_queryset(self.get_queryset())  # Применение фильтров и сортировки
        # Если нужно, можно добавить пагинацию данных:
        # page = self.paginate_queryset(queryset)  # Пагинация данных
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)  # Если пагинация не используется
        return Response(serializer.data)


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

