from drf_spectacular.utils import extend_schema, extend_schema_view
from clients.models.deals import Deal
from clients.serializers.api.deal import (
    DealCreateSerializer,
    DealUpdateSerializer,
    DealListSerializer,
    DealDeleteSerializer,
)
from common.views import CLUDViewSet


@extend_schema_view(
    create=extend_schema(
        summary='Создать сделку',
        description='Создает новую сделку и автоматически назначает менеджера',
        tags=['🤝 Сделки'],
    ),
    partial_update=extend_schema(
        summary='Обновить сделку',
        description='Частично обновляет информацию о сделке',
        tags=['🤝 Сделки'],
    ),
    list=extend_schema(
        summary='Список сделок',
        description='Получает список всех сделок',
        tags=['🤝 Сделки'],
    ),
    destroy=extend_schema(
        summary='Удалить сделку',
        description='Удаляет указанную сделку',
        tags=['🤝 Сделки'],
    )
)
class DealView(CLUDViewSet):
    """
    Представление для работы со сделками.
    Позволяет создавать, редактировать, удалять и просматривать сделки.
    """
    queryset = Deal.objects.all()
    http_method_names = ('post', 'get', 'patch', 'delete')
    multi_serializer_class = {
        'create': DealCreateSerializer,
        'partial_update': DealUpdateSerializer, # нужно переопределить метод update для вложенного сериализатора
        'list': DealListSerializer,
        'destroy': DealDeleteSerializer,
    }

    def perform_create(self, serializer: DealCreateSerializer) -> None:
        """
        Автоматически назначает текущего пользователя менеджером сделки перед сохранением.
        """
        serializer.save(manager=self.request.user)

