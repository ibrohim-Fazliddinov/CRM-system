from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from clients.models.client import Client
from clients.models.deals import Deal
from clients.serializers.api.client import ClientListSerializer
from clients.serializers.nested.client import ClientSHortSerializer


class BaseDealSerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор для модели Deal.
    Определяет общие поля для всех наследуемых сериализаторов.
    """
    class Meta:
        model = Deal
        fields = (
            'id',
            'name',
            'status_deal',
            'amount',
        )


class DealListSerializer(BaseDealSerializer):
    """
    Сериализатор для получения списка сделок.
    Включает информацию о клиенте.
    """
    client = ClientListSerializer()

    class Meta(BaseDealSerializer.Meta):
        fields = BaseDealSerializer.Meta.fields + ('client',)


class DealUpdateSerializer(DealListSerializer):
    """
    Сериализатор для обновления сделок.
    Наследуется от DealListSerializer.
    """
    pass


class DealCreateSerializer(BaseDealSerializer):
    """
    Сериализатор для создания новой сделки.
    Поддерживает чтение информации о клиенте и запись через client_id.
    """
    client = ClientSHortSerializer(read_only=True)  # Поле для ответа (только для чтения)
    client_id = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all(), source='client', write_only=True  # Поле для запроса (только для записи)
    )

    class Meta(BaseDealSerializer.Meta):
        fields = BaseDealSerializer.Meta.fields + ('client', 'client_id')

    def validate(self, attrs):
        """
        Валидация на количество активных сделок у клиента.
        Проверяется, что у клиента не больше 3 сделок со статусом "В работе".
        """
        client = attrs.get('client') or self.context['request'].user.client
        if client:
            # Проверяем количество активных сделок клиента со статусом "В работе"
            deal_count = Deal.objects.filter(client=client, status_deal='PRG').count()
            if deal_count >= 3:
                raise ValidationError(
                    {'client': 'У клиента уже есть 3 активные сделки, нельзя добавить больше.'}
                )
        return attrs

    def validate_amount(self, value):
        """
        Проверяет, что сумма сделки больше нуля.
        """
        if value <= 0:
            raise serializers.ValidationError("Сумма сделки должна быть больше нуля.")
        return value


class DealDeleteSerializer(serializers.ModelSerializer):
    """
    Сериализатор для удаления сделки.
    Использует все поля модели Deal.
    """
    class Meta:
        model = Deal
        fields = '__all__'


