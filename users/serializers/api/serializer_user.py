from crum import get_current_user
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from djoser import serializers as dj_serializers
from rest_framework import serializers
from rest_framework.exceptions import ParseError, ValidationError

User = get_user_model()

class RegistrationsSerializer(dj_serializers.UserCreateSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
    )

    @staticmethod
    def validate_email(value: str) -> str:
        """
        Валидирует email, проверяя, что пользователь с таким email еще не существует.
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
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs: dict[str, str]) -> dict[str, str]:
        """Проверка на корректность пароля."""
        user = get_current_user()
        old_password = attrs.pop('old_password')
        if not user.check_password(raw_password=old_password):
            raise ParseError('')
        return attrs

    @staticmethod
    def validate_new_password(password: str) -> str:
        validate_password(password)
        return password

    def update(self, instance: User, validated_data: dict[str, str]) -> User:
        password = validated_data.pop('new_password')
        instance.set_password(password)
        instance.save()
        return instance


    class Meta:
        model = User
        fields = (
            'old_password',
            'new_password',
        )

class UserSearchListSerializer(serializers.ModelSerializer):

    class Meta:
        models = User
        fields = (
            'id',
            'username',
            'email',
            'get_full_name'
        )

class CustomActivationSerializer(dj_serializers.ActivationSerializer):
    """Сериализатор для активации пользователя"""
    pass
class CustomResetPasswordSerializer(dj_serializers.SendEmailResetSerializer):
    pass

class CustomResetPasswordConfirmSerializer(dj_serializers.PasswordResetConfirmSerializer):
    pass

# class UserUpdateSerializer(serializers.ModelSerializer):
#     pass