from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from typing import Optional, Union
from django.conf import settings
from users.serializers.api.serializer_user import CustomResetPasswordConfirmSerializer
from users.services.tasks import tasks

User = get_user_model()

class UserResetPasswordService:
    """Сервисная часть для запроса о новом пароле."""

    def __init__(
        self, user: User, context: Optional[dict[str, Union[str, int]]]
    ) -> None:
        """Инициализация активации пользователя."""
        self._user = user
        self._context = context or {}

    def _send_email_user_reset_password(self) -> None:
        """Отправить по электронной почте новый пароль."""
        if self._user.email:  # Проверяем, что у пользователя есть email
            tasks.send_reset_password_task.delay(self._context, [self._user.email])

    def execute(self) -> None:
        """Выполнить отправку нового пароля."""
        if self._user is not None:
            self._send_email_user_reset_password()

class UserResetPasswordConfirmService:
    """Сервисная часть для сброса пароля и установления нового."""

    def __init__(
        self,
        user: User,
        serializer: CustomResetPasswordConfirmSerializer,
        context: Optional[dict[str, Union[str, int]]],
    ) -> None:
        """Инициализация класса сброса пароля и установления нового."""
        self._user = user
        self._serializer = serializer
        self._context = context or {}

    def _set_password(self) -> None:
        """Установить новый пароль."""
        self._user.set_password(self._serializer.validated_data['new_password'])

    def _update_user_data(self) -> None:
        """Обновить данные пользователя и сохранить."""
        if hasattr(self._user, 'last_login'):
            self._user.last_login = timezone.now()
        self._user.save()

    def _send_email_user_reset_password_confirm(self) -> None:
        """Отправить по электронной почте подтверждение сброса пароля."""
        if self._user.email and settings.PASSWORD_CHANGED_EMAIL_CONFIRMATION:
            tasks.send_reset_password_confirm_task.delay(self._context, [self._user.email])

    def execute(self) -> None:
        """Выполнить сброс пароля и установить новый."""
        with transaction.atomic():
            self._set_password()
            self._update_user_data()

        self._send_email_user_reset_password_confirm()
