import logging
from typing import Union

from django.core.exceptions import ObjectDoesNotExist

from common.celery import app
from django.contrib.auth import get_user_model
from djoser import email as djoser_email

User = get_user_model()

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
        if self._user.email and settings.DJOSER.get('PASSWORD_CHANGED_EMAIL_CONFIRMATION', False):
            tasks.send_reset_password_confirm_task.delay(self._context, [self._user.email])

    def execute(self) -> None:
        """Выполнить сброс пароля и установить новый."""
        with transaction.atomic():
            self._set_password()
            self._update_user_data()

        self._send_email_user_reset_password_confirm()
# region --------------------------- AUTHORISATION ----------------------------------
@app.task(bind=True, default_retry_delay=5 * 60)
def send_reset_password_task(
        self,
        context: dict[str, Union[str, int]],
        email: list[str],
) -> None:
    """Задача на отправку электронного письма для нового пароля."""
    try:
        context['user'] = User.objects.get(id=context.get('user_id'))
        djoser_email.PasswordResetEmail(context=context).send(email)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)


@app.task(bind=True, default_retry_delay=5 * 60)
def send_activation_task(
        self,
        context: dict[str, Union[str, int]],
        email: list[str],
) -> None:
    """Задача на отправку электронного письма об активации пользователя."""
    try:
        context['user'] = User.objects.get(id=context.get('user_id'))
        djoser_email.ActivationEmail(context=context).send(email)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)


@app.task(bind=True, default_retry_delay=5 * 60)
def send_reset_password_confirm_task(
        self,
        context: dict[str, Union[str, int]],
        email: list[str]
) -> None:
    """
    Задача на отправку электронного письма о сбросе пароля
    и изменение его на новый.
    """
    try:
        context['user'] = User.objects.get(id=context.get('user_id'))
        djoser_email.PasswordChangedConfirmationEmail(context=context).send(email)
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)
# endregion -------------------------------------------------------------------------

logger = logging.getLogger(__name__)

@app.task(bind=True, default_retry_delay=5 * 60)
def send_reset_password_task(self, context: dict[str, Union[str, int]], email: list[str]) -> None:
    """Задача на отправку электронного письма для нового пароля."""
    try:
        user_id = context.get("user_id")
        if user_id is None:
            logger.error("send_reset_password_task: user_id отсутствует в контексте")
            return

        try:
            context["user"] = User.objects.get(id=user_id)
        except ObjectDoesNotExist:
            logger.error(f"send_reset_password_task: Пользователь с id={user_id} не найден")
            return

        djoser_email.PasswordResetEmail(context=context).send(email)

    except Exception as exc:
        logger.exception("Ошибка при отправке email на сброс пароля")
        raise self.retry(exc=exc, countdown=60)