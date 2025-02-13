from typing import Optional, Union
from crum import get_current_user
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from djoser.conf import settings
from djoser.serializers import ActivationSerializer
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from common.views import ExtendedUserViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from users.serializers.api.serializer_user import (
    RegistrationsSerializer,
    UserSearchListSerializer,
    UserListSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer,
    CustomResetPasswordSerializer,
    CustomResetPasswordConfirmSerializer,
)
from users.services.tasks.tasks import UserResetPasswordConfirmService, UserResetPasswordService

User = get_user_model()

def get_context(
        user: User, request: Request, send_email: bool
) -> Optional[dict[str, Union[str, int]]]:
    """Получить контекст для отправки электронного письма."""
    if send_email:
        context = {
            'user_id': user.pk,
            'domain': request.get_host(),
            'protocol': 'https' if request.is_secure() else 'http',
            'site_name': request.get_host(),
        }
        return context

@extend_schema_view(
    registration=extend_schema(
        summary='Регистрация нового пользователя.',
        tags=['👤 Пользователь']
    ),
    activate=extend_schema(
        summary='Активация учетной записи пользователя.',
        tags=['👤 Пользователь']
    ),
    user_search=extend_schema(
        summary='Поиск пользователей по заданным фильтрам.',
        tags=['👤 Пользователь']
    ),
    user_list=extend_schema(
        summary='Получение списка пользователей.',
        tags=['👤 Пользователь']
    ),
    user_update=extend_schema(
        summary='Обновление данных пользователя.',
        tags=['👤 Пользователь']
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
    def user_search(self) -> Response:
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
        summary='Смена пароля пользователя.',
        tags=['🔐 Пароль'],
    ),
    reset_password=extend_schema(
        summary='Запрос на сброс пароля.',
        tags=['🔐 Пароль'],
    ),
    reset_password_confirm=extend_schema(
        summary='Подтверждение сброса пароля.',
        tags=['🔐 Пароль'],
    )
)
class PasswordChangingView(ExtendedUserViewSet):
    """
    Представление для управления паролями пользователей.

    Данный viewset предоставляет функциональность смены пароля,
    запроса на сброс пароля и подтверждения сброса пароля.
    """

    serializer_class = ChangePasswordSerializer()
    multi_serializer_class = {
        'change_password': ChangePasswordSerializer,
        'reset_password': CustomResetPasswordSerializer,
        'reset_password_confirm': CustomResetPasswordConfirmSerializer
    }

    @action(methods=['POST'], detail=False)
    def change_password(self, request: Request) -> Response:
        """
        Смена пароля текущего аутентифицированного пользователя.

        - Получает текущего пользователя из контекста.
        - Проверяет валидность данных через сериализатор.
        - Сохраняет новый пароль.
        - Возвращает статус 204 (успешное выполнение без контента).

        :param request: Объект HTTP-запроса с новыми данными пароля.
        :return: HTTP 204 No Content в случае успеха.
        """
        user = get_current_user()
        serializer = self.get_serializer(instance=user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['POST'], detail=False)
    def reset_password(self, request: Request, *args: None, **kwargs: None) -> Response:
        """
        Инициирует процесс сброса пароля для пользователя.

        - Проверяет валидность введённых данных.
        - Получает текущего пользователя (если авторизован) или ищет по email.
        - Создаёт контекст для email-уведомления.
        - Запускает сервис сброса пароля, отправляя письмо с инструкциями.
        - Возвращает HTTP 204 No Content в случае успеха.

        :param request: Объект HTTP-запроса с email пользователя.
        :return: HTTP 204 No Content, если письмо отправлено.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_current_user()
        context = get_context(user, request, bool(user))
        reset_password = UserResetPasswordService(user, context)
        reset_password.execute()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['POST'], detail=False)
    def reset_password_confirm(self, request: Request, *args: None, **kwargs: None) -> Response:
        """
        Подтверждение сброса пароля с помощью кода или токена.

        - Проверяет валидность переданных данных (код сброса, новый пароль).
        - Определяет пользователя по токену или коду.
        - Создаёт контекст для email-уведомления.
        - Запускает сервис подтверждения сброса пароля.
        - Возвращает HTTP 204 No Content в случае успеха.

        :param request: Объект HTTP-запроса с токеном/кодом и новым паролем.
        :return: HTTP 204 No Content после успешного сброса пароля.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        context = get_context(
            user=user,
            request=request,
            send_email=settings.DJOSER.get('PASSWORD_CHANGED_EMAIL_CONFIRMATION', False),
        )
        reset_password_confirm = UserResetPasswordConfirmService(
            user=user, context=context, serializer=serializer,
        )
        reset_password_confirm.execute()
        return Response(status=status.HTTP_204_NO_CONTENT)
