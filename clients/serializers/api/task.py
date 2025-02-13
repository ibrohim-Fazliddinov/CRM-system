from rest_framework import serializers
from clients.models.deals import Deal
from clients.models.model_tk import Task
from clients.serializers.api.deal import DealListSerializer, BaseDealSerializer
from clients.serializers.nested.client import ClientSHortSerializer


class TaskListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для получения списка задач.

    Включает информацию о клиенте и сделке.
    """
    client = ClientSHortSerializer()
    deal = BaseDealSerializer()

    class Meta:
        model = Task
        fields = (
            'id',
            'name',
            'description',
            'priority',
            'status_task',
            'due_date',
            'deal',
            'client',
            'created_by',
            'updated_by',
        )


class TaskCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания задачи.

    - `deal` — отображает связанную сделку (только для чтения).
    - `deal_id` — принимает ID сделки при создании задачи.
    """
    deal = DealListSerializer(read_only=True)  # Поле для ответа (только для чтения)
    deal_id = serializers.PrimaryKeyRelatedField(
        queryset=Deal.objects.all(), source='deal', write_only=True  # Поле для запроса (только для записи)
    )

    class Meta:
        model = Task
        fields = (
            'id',
            'name',
            'description',
            'status_task',
            'due_date',
            'priority',
            'deal',
            'deal_id',
        )


class TaskUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления задачи.

    - `deal` — отображает связанную сделку (только для чтения).
    """
    deal = DealListSerializer(read_only=True)

    class Meta:
        model = Task
        fields = (
            'id',
            'name',
            'description',
            'status_task',
            'priority',
            'due_date',
            'deal',
        )


class TaskDeleteSerializer(serializers.ModelSerializer):
    """
    Сериализатор для удаления задачи.

    Возвращает все поля объекта перед удалением.
    """

    class Meta:
        model = Task
        fields = '__all__'
