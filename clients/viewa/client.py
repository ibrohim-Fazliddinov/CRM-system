from typing import Any
from clients.serializers.api.client import (
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
from clients.models.client import Client

@extend_schema_view(
    search=extend_schema(
        summary='Поиск клиента',
        tags=['👥 Клиенты']
    ),
    list=extend_schema(
        summary='Получить список клиентов',
        tags=['👥 Клиенты']
    ),
    create=extend_schema(
        summary='Регистрация нового клиента',
        tags=['👥 Клиенты']
    ),
    partial_update=extend_schema(
        summary='Обновление информации о клиенте',
        tags=['👥 Клиенты']
    ),
    update=extend_schema(
        summary='Обновление информации о клиенте',
        tags=['👥 Клиенты']
    ),
    destroy=extend_schema(
        summary='Удаление клиента',
        tags=['👥 Клиенты']
    ),
    retrieve=extend_schema(
        summary='Просмотр клиента',
        tags=['👥 Клиенты']
    )
)
class ClientView(CRUDListViewSet):
    """
    Набор представлений для управления клиентами.

    Этот класс предоставляет функционал для создания, обновления, удаления, поиска и получения списка клиентов.

    Атрибуты:
        queryset (QuerySet): Набор данных, содержащий всех клиентов.
        multi_serializer_class (dict): Словарь сериализаторов, используемых для различных действий (создание, поиск, обновление, удаление, получение списка и одного объекта).

    Методы:
        search: Выполняет поиск клиентов по заданным параметрам.
        client_list: Возвращает список всех клиентов.
        client_create: Регистрация нового клиента.
        client_update: Обновление информации о клиенте.
        client_delete: Удаление клиента.
    """

    queryset = Client.objects.all()
    serializer_class = ClientListSerializer
    multi_serializer_class = {
        'create': CreateClientSerializer,
        'client_search': ClientSearchSerializer,
        'list': ClientListSerializer,
        'update': ClientUpdateSerializer,
        'partial_update': ClientUpdateSerializer,
        'delete': ClientDeleteSerializer,
        'retrieve': ClientListSerializer,
    }

    @action(methods=['GET'], detail=False, url_path='search')
    def search(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Выполняет поиск клиентов по заданным параметрам фильтрации.

        Параметры:
            request (Request): Объект запроса, содержащий параметры для фильтрации клиентов.

        Возвращает:
            Response: Объект с сериализованными данными клиентов, соответствующих условиям поиска.
        """
        return super().list(request, *args, **kwargs)



