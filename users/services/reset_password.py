from typing import Optional, Union
from venv import logger

from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from config import settings
from users.serializers.api.serializer_user import CustomResetPasswordSerializer, CustomResetPasswordConfirmSerializer

User = get_user_model()

class UserResetPasswordService:
    pass

class UserResetPasswordConfirmService:
    def __init__(
            self,
            user: User,
            serializer: CustomResetPasswordConfirmSerializer,
            context: Optional[dict[str, Union[str, int]]]
    ) -> None:
        self._user = user
        self._serializer = serializer
        self._context = context

    def _set_password(self) -> None:
        new_password = self._serializer.validated_data.get('new_password')
        if not new_password:
            raise ValueError('')
        self._user.set_password(new_password)

    def _is_has_last_login(self) -> None:
        if hasattr(self._user, 'last_login'):
            self._user.last_login = timezone.now()

    def _user_save(self) -> None:
        self._user.save()

    def _send_email_reset_password_confirm(self) -> None:
        try:
            pass
        except Exception as e:
            logger.error(f"Ошибка при сбросе пароля: {e}")
            raise

    def execute(self) -> None:
        try:
            with transaction.atomic():
                self._set_password()
                self._is_has_last_login()
                self._user_save()
            if settings:
                pass
            logger.info(f"Пароль успешно обновлен для пользователя: {self._user.email}")
        except Exception as e:
            logger.error(f"Ошибка при сбросе пароля: {e}")
            raise


