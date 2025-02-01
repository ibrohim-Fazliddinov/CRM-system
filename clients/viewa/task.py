from drf_spectacular.utils import extend_schema_view, extend_schema
from requests import delete

from clients.models.tasks import Task
from clients.serializers.api.task import TaskCreateSerializer, TaskUpdateSerializer, TaskListSerializer, \
    TaskDeleteSerializer
from common.views import CLUDViewSet

@extend_schema_view(
    create=extend_schema(
        summary='', tags=['📄Задачи']
    ),
    update=extend_schema(
        summary='', tags=['📄Задачи']
    ),
    partial_update=extend_schema(
        summary='', tags=['📄Задачи']
    ),
    destroy=extend_schema(
        summary='', tags=['📄Задачи']
    ),
    list=extend_schema(
        summary='', tags=['📄Задачи']
    ),
)
class TaskView(CLUDViewSet):
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
        Автоматически назначает текущего пользователя менеджером сделки перед сохранением.
        """
        serializer.save(manager=self.request.user)
