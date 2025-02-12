import logging
from typing import Union

from django.core.exceptions import ObjectDoesNotExist

from common.celery import app
from django.contrib.auth import get_user_model
from djoser import email as djoser_email

User = get_user_model()


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