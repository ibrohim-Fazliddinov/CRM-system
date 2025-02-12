import binascii
import os
from tempfile import template

from django.contrib.auth import get_user_model
from django.db import models
from django.template.defaultfilters import random
from common.models.mixins import DateMixin
from sendpulse.models import Template

User = get_user_model()

class EmailConfirmToken(DateMixin):
    """
        Модель токена подтверждения email.

        Поля:
            user (ForeignKey): Ссылка на пользователя, для которого создан токен.
            key (CharField): Уникальный шестнадцатеричный токен, используемый для подтверждения email.

        Атрибуты:
            - `max_length=64`: Максимальная длина токена установлена с запасом.
            - `unique=True`: Гарантирует, что каждый токен уникален.
            - `db_index=True`: Улучшает производительность поиска токена в базе данных.
            - `verbose_name='Token'`: Читабельное название для админки.

        Примеры использования:
            # Создание нового токена для пользователя
            >>> user = User.objects.get(email="user@example.com")
            >>> token = EmailConfirmToken.objects.create(user=user, key=EmailConfirmToken.generate_key())

            # Проверка токена
            >>> found_token = EmailConfirmToken.objects.filter(key="a3b1c4d5e6").first()
            >>> if found_token:
            ...     print("Токен найден!")

        """
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='email_confirm_token'
    )
    key = models.CharField(
        max_length=32,
        db_index=True,
        unique=True,verbose_name='Token'
    )

    @staticmethod
    def generate_key():

        """
               Генерирует случайный токен для подтверждения email.

               Алгоритм:
               1. Генерирует случайное число `len_of_token` от 10 до 32 (определяет длину токена).
               2. Создает 16 случайных байтов с помощью os.urandom(16).
               3. Конвертирует их в шестнадцатеричную строку с помощью binascii.hexlify.
               4. Декодирует байты в строку и обрезает до `len_of_token` символов.

               Возвращает:
                   str: случайный шестнадцатеричный токен длиной от 10 до 32 символов.

               Примеры использования:
                   >>> token = EmailConfirmToken.generate_key()
                   >>> print(token) # 'a3b1c4d5e6' (пример)
               """
        len_of_token = random.randint(10, 32)
        return binascii.hexlify(os.urandom(16)).decode()[0:len_of_token]

    def save(self, *args, **kwargs) -> None:
        if not self.key:
            self.key = self.generate_key()
        return super(EmailConfirmToken, self).save(*args, **kwargs)

    def __str__(self):
        return f'Токен {self.user}'

    def confirm_email_send(self):
        template = Template

class ResetPasswordToken:
    user = models.ForeignKey()