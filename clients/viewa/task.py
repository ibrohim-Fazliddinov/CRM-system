from drf_spectacular.utils import extend_schema_view, extend_schema
from clients.models.model_tk import Task
from clients.serializers.api.task import (
    TaskCreateSerializer,
    TaskUpdateSerializer,
    TaskListSerializer,
    TaskDeleteSerializer
)
from common.views import CLUDViewSet


@extend_schema_view(
    create=extend_schema(
        summary='Создание новой задачи', tags=['📄 Задачи']
    ),
    update=extend_schema(
        summary='Обновление задачи', tags=['📄 Задачи']
    ),
    partial_update=extend_schema(
        summary='Частичное обновление задачи', tags=['📄 Задачи']
    ),
    destroy=extend_schema(
        summary='Удаление задачи', tags=['📄 Задачи']
    ),
    list=extend_schema(
        summary='Получение списка задач', tags=['📄 Задачи']
    ),
)
class TaskView(CLUDViewSet):
    """
    Представление для управления задачами.

    Доступные действия:
    - Создание задачи
    - Обновление задачи
    - Частичное обновление задачи
    - Удаление задачи
    - Получение списка задач
    """

    queryset = Task.objects.all()
    multi_serializer_class = {
        'create': TaskCreateSerializer,
        'update': TaskUpdateSerializer,
        'partial_update': TaskUpdateSerializer,
        'list': TaskListSerializer,
        'delete': TaskDeleteSerializer,
    }

    def perform_create(self, serializer: TaskCreateSerializer) -> None:
        """
        Автоматически назначает текущего пользователя менеджером задачи перед сохранением.

        :param serializer: Сериализатор для создания задачи.
        """
        serializer.save(manager=self.request.user)

