from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models


from common.models.mixins import InfoMixin
from common.models.models import BaseModel

User= get_user_model()

class Client(BaseModel, InfoMixin):
    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    company = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Компания'
    )
    address = models.TextField(
        blank=True,
        null=True,
        verbose_name='Адрес'
    )
    manager = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="clients",
        verbose_name='Менеджер',
    )
    is_active_client = models.BooleanField(default=True, verbose_name='Активный клиент')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'Client:{self.pk}|{self.email} -  Manager:{self.manager}'
