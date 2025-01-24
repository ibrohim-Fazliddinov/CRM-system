from django.db import transaction
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from clients.models.client import Client
from users.serializers.api.serializer_user import UserListSerializer
User = get_user_model()

class ClientSearchSerializer(serializers.ModelSerializer):
    """
    Сериализатор для поиска клиентов.
    Используется для отображения минимального набора данных о клиенте.
    """
    manager = UserListSerializer()

    class Meta:
        model = Client
        fields = (
            'id',
            'email',
            'manager',
        )

class ClientListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения списка клиентов.
    Содержит расширенный набор данных о клиенте.
    """
    manager = UserListSerializer()

    class Meta:
        model = Client
        fields = (
            'id',
            'name',
            'email',
            'manager',
            'company',
            'address',
            'created_by',
            'created_at',
            'notes',
        )

class CreateClientSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания клиента.
    Поддерживает ввод пароля и проверку email на уникальность.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Client
        fields = (
            'id',
            'email',
            'name',
            'password',
        )

    @staticmethod
    def validate_email(value: str) -> str:
        """
        Проверяет, что пользователь с указанным email еще не зарегистрирован.

        :param value: Введенный email.
        :return: Валидированный email.
        :raises ValidationError: Если пользователь с таким email уже существует.
        """
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с такой почтой уже зарегистрирован!')
        return email

    def create(self, validated_data):
        """
        Создает нового клиента с привязкой менеджера к текущему пользователю.

        :param validated_data: Валидированные данные для создания клиента.
        :return: Экземпляр клиента.
        """
        validated_data.pop('password')

        with transaction.atomic():
            # Привязка менеджера к текущему пользователю
            validated_data['manager'] = self.context['request'].user
            # Создание экземпляра клиента
            instance = super().create(validated_data)
        return instance

class ClientUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления информации о клиенте.
    Содержит базовые поля для редактирования.
    """

    class Meta:
        model = Client
        fields = (
            'id',
            'name',
            'email',
            'company',
            'address',
            'notes',
        )

    def validate_email(self, value: str) -> str:
        """
        Проверяет, что новый email не принадлежит другому пользователю.

        :param value: Введенный email.
        :return: Валидированный email.
        :raises ValidationError: Если email уже используется.
        """
        email = value.lower()
        if Client.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise ValidationError('Этот email уже используется другим клиентом!')
        return email

class ClientDeleteSerializer(serializers.ModelSerializer):
    """
    Сериализатор для удаления клиента.
    Содержит все поля модели для проверки данных перед удалением.
    """

    class Meta:
        model = Client
        fields = '__all__'
