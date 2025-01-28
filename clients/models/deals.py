from django.contrib.auth import get_user_model
from django.db import models

from clients.models.client import Client
from common.models.mixins import InfoMixin
from common.models.models import BaseModel

User = get_user_model()

class Deal(BaseModel, InfoMixin):
    STATUS_CHOICES = [
        ('NEW', 'Новая'),
        ('PRG', 'В работе'),
        ('COM', 'Завершена'),
    ]

    name = models.CharField(
        max_length=255,
        verbose_name='Название сделки'
    )
    status = models.CharField(
        max_length=3,
        choices=STATUS_CHOICES,
        default='NEW',
        verbose_name='Статус сделки'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Сумма сделки'
    )
    manager = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='deal_manager',
        verbose_name='Ответственный менеджер'
    )
    client = models.ForeignKey(
        to=Client,
        on_delete=models.CASCADE,
        related_name='deal_client',
        verbose_name='Клиент'
    )

    class Meta:
        verbose_name = 'Сделка'
        verbose_name_plural = 'Сделки'

    def __str__(self):
        return f'{self.name} ({self.get_status_display()})'

