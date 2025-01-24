from typing import Any

from rest_framework import status
from clients.serializers.api.serializer_user import (
    ClientListSerializer,
    CreateClientSerializer,
    ClientSearchSerializer,
    ClientUpdateSerializer,
    ClientDeleteSerializer
)
from common.views import CRUDListViewSet
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from .models import Client

@extend_schema_view(
    search=extend_schema(
        summary='Поиск клиента',
        tags=['Клиенты']
    ),
    client_list=extend_schema(
        summary='Получить список клиентов',
        tags=['Клиенты']
    ),
    client_create=extend_schema(
        summary='Регистрация нового клиента',
        tags=['Клиенты']
    ),
    client_update=extend_schema(
        summary='Обновление информации о клиенте',
        tags=['Клиенты']
    ),
    client_delete=extend_schema(
        summary='Удаление клиента',
        tags=['Клиенты']
    )
)
class ClientView(CRUDListViewSet):
    """
    Набор представлений для управления клиентами.

    Этот класс включает методы для создания, обновления, удаления, поиска и получения списка клиентов.

    Атрибуты:
        queryset (QuerySet): Набор данных, содержащий всех клиентов.
        serializer_class (Serializer): Основной сериализатор для отображения списка клиентов.
        multi_serializer_class (dict): Словарь сериализаторов для различных действий (создание, поиск, обновление, удаление).

    Методы:
        search: Поиск клиентов по заданным параметрам.
        client_list: Получение списка всех клиентов.
        client_create: Регистрация нового клиента.
        client_update: Обновление информации о клиенте.
        client_delete: Удаление клиента.
    """

    queryset = Client.objects.all()
    serializer_class = ClientListSerializer

    multi_serializer_class = {
        'client_create': CreateClientSerializer,
        'client_search': ClientSearchSerializer,
        'client_update': ClientUpdateSerializer,
        'client_delete': ClientDeleteSerializer,
    }

    @action(methods=['GET'], detail=False, url_path='search')
    def search(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Поиск клиентов по заданным параметрам.

        Параметры:
            request (Request): Объект запроса, содержащий параметры для фильтрации.

        Возвращает:
            Response: Сериализованный список клиентов, соответствующих заданным фильтрам.
        """
        return super().list(request, *args, **kwargs)

    @action(methods=['GET'], detail=False)
    def client_list(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Получение списка всех клиентов.

        Параметры:
            request (Request): Объект запроса.

        Возвращает:
            Response: Сериализованный список всех клиентов.
        """
        return self.retrieve(request, *args, **kwargs)

    @action(methods=['POST'], detail=False)
    def client_create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Регистрация нового клиента.

        Используется сериализатор CreateClientSerializer для валидации и создания нового клиента.

        Параметры:
            request (Request): Объект запроса, содержащий данные для создания клиента.

        Возвращает:
            Response: Ответ с результатом операции создания клиента.
        """
        return self.create(request, *args, **kwargs)

    @action(methods=['PUT', 'PATCH'], detail=False)
    def client_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Обновление информации о клиенте.

        Поддерживает полный (PUT) и частичный (PATCH) методы обновления. Используется соответствующий сериализатор ClientUpdateSerializer.

        Параметры:
            request (Request): Объект запроса, содержащий данные для обновления клиента.

        Возвращает:
            Response: Ответ с результатом обновления информации о клиенте.
        """
        if request.method == 'PUT':
            return self.update(request, *args, **kwargs)
        elif request.method == 'PATCH':
            return self.partial_update(request, *args, **kwargs)

    @action(methods=['DELETE'], detail=True)
    def client_delete(self, request: Request, pk: int = None) -> Response:
        """
        Удаление клиента по идентификатору.

        Параметры:
            request (Request): Объект запроса.
            pk (int, optional): Идентификатор клиента, которого необходимо удалить.

        Возвращает:
            Response: Ответ с подтверждением успешного удаления.
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'detail': 'Клиент успешно удален.'}, status=status.HTTP_204_NO_CONTENT)

