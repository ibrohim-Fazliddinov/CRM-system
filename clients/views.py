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

    Содержит методы для создания, поиска, обновления и получения списка клиентов.
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
    def search(self, request, *args, **kwargs):
        """
        Метод для поиска клиентов.

        Параметры:
            request: объект запроса, содержащий параметры для фильтрации.

        Возвращает:
            Response: Сериализованный список найденных клиентов.
        """
        return super().list(request, *args, **kwargs)

    @action(methods=['GET'], detail=False)
    def client_list(self, request: Request, *args: None, **kwargs: None) -> Response:
        """
        Метод для получения списка сотрудников.

        Использует стандартный метод retrieve для получения списка всех сотрудников.

        Параметры:
            request: объект запроса, содержащий параметры фильтрации (если применимо).

        Возвращает:
            Response: Сериализованный список сотрудников.
        """
        return self.retrieve(request, *args, **kwargs)

    @action(methods=['POST'], detail=False)
    def client_create(self, request: Request, *args: None, **kwargs: None) -> Response:
        """
        Метод для регистрации нового сотрудника.

        Использует сериализатор CreateClientSerializer для валидации и создания записи.

        Параметры:
            request: объект запроса, содержащий данные для регистрации нового сотрудника.

        Возвращает:
            Response: Ответ с результатом создания нового сотрудника.
        """
        return self.create(request, *args, **kwargs)

    @action(methods=['PUT', 'PATCH'], detail=False)
    def client_update(self, request: Request, *args, **kwargs) -> Response:
        """
        Метод для обновления информации о сотруднике.

        Поддерживает полный (PUT) и частичный (PATCH) методы обновления.

        Параметры:
            request: объект запроса, содержащий данные для обновления.

        Возвращает:
            Response: Ответ с результатом обновления информации о сотруднике.
        """
        update_methods = {'PUT': self.update, 'PATCH': self.partial_update}
        for method, func in update_methods.items():
            if method == request.method:
                return func(request, *args, **kwargs)

    @action(methods=['DELETE'], detail=True)  # detail=True, для работы с объектом по его pk
    def client_delete(self, request: Request, pk=None) -> Response:
        """Удаление конкретного объекта"""
        instance = self.get_object()  # Получение объекта по pk
        self.perform_destroy(instance)
        return Response({'detail': 'Объект успешно удален.'}, status=status.HTTP_204_NO_CONTENT)
