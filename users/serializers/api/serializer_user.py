from typing import Optional
from crum import get_current_user
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from djoser import serializers as dj_serializers
from rest_framework import serializers
from rest_framework.exceptions import ParseError, ValidationError
from django.db import transaction
from users.models.profile import Profile
from users.serializers.nested.serializer_profile import ProfileUpdateSerializer, ProfileShortSerializer

User = get_user_model()

class RegistrationsSerializer(dj_serializers.UserCreateSerializer):
    """
    Сериализатор для регистрации нового пользователя.
    """
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
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

    class Meta:
        model = User
        fields = (
            'id',
            'get_full_name',
            'email',
            'password',
        )


class ChangePasswordSerializer(serializers.ModelSerializer):
    """
    Сериализатор для изменения пароля пользователя.
    """
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'old_password',
            'new_password',
        )

    def validate(self, attrs: dict[str, str]) -> dict[str, str]:
        """
        Проверяет правильность текущего пароля пользователя.

        :param attrs: Данные для проверки.
        :return: Валидированные данные.
        :raises ParseError: Если текущий пароль неверен.
        """
        user = get_current_user()
        old_password = attrs.pop('old_password')
        if not user:
            raise ValidationError("User not found")
        if not user.check_password(old_password):
            raise ParseError('Неверный текущий пароль.')
        return attrs

    @staticmethod
    def validate_new_password(password: str) -> str:
        """
        Валидирует новый пароль согласно стандартным правилам.

        :param password: Новый пароль.
        :return: Валидированный пароль.
        """
        validate_password(password)
        return password

    def update(self, instance: User, validated_data: dict[str, str]) -> User:
        """
        Обновляет пароль пользователя.

        :param instance: Текущий пользователь.
        :param validated_data: Валидированные данные.
        :return: Обновленный пользователь.
        """
        password = validated_data.pop('new_password')
        instance.set_password(password)
        instance.save()
        return instance


class UserSearchListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для поиска пользователей.
    """
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name'
        )


class CustomActivationSerializer(dj_serializers.ActivationSerializer):
    """
    Сериализатор для активации пользователя.
    """
    pass


# class CustomResetPasswordSerializer(dj_serializers.SendEmailResetSerializer):
#     """
#     Сериализатор для отправки email для сброса пароля.
#     """
#     pass
#
#
# class CustomResetPasswordConfirmSerializer(dj_serializers.PasswordResetConfirmSerializer):
#     """
#     Сериализатор для подтверждения сброса пароля.
#     """
#     pass


class UserListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отображения списка пользователей.
    """
    profile = ProfileShortSerializer()

    class Meta:
        model = User
        fields = (
            'id',
            'get_full_name',
            'email',
            'profile',
        )


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления данных пользователя.

    """
    profile = ProfileUpdateSerializer()

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'profile',
        )

    @staticmethod
    def _update_profile(profile: Profile, data: Optional[str]) -> None:
        """
        Обновляет данные профиля пользователя.

        :param profile: Объект профиля.
        :param data: Данные для обновления.
        """
        profile_serializer = ProfileUpdateSerializer(
            instance=profile, data=data, partial=True
        )
        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save()

    def update(self, instance: User, validated_data: dict[str, str]) -> User:
        """
        Обновляет данные пользователя и связанные данные профиля.

        :param instance: Текущий пользователь.
        :param validated_data: Валидированные данные.
        :return: Обновленный пользователь.
        """
        profile_data = validated_data.pop('profile') if 'profile' in validated_data else None

        with transaction.atomic():
            instance = super().update(
                instance=instance,
                validated_data=validated_data
            )
            if profile_data:
                self._update_profile(instance.profile, profile_data)
        return instance
