from django.contrib.auth import get_user_model
from django.db import models
from clients.models.client import Client
from clients.models.deals import Deal
from common.models.mixins import InfoMixin
from common.models.models import BaseModel

User = get_user_model()

class Task(BaseModel, InfoMixin):
    PRIORITY_CHOICES = [
        ('LOW', 'Низкий'),
        ('MID', 'Средний'),
        ('HIG', 'Высокий'),
    ]
    STATUS_CHOICES_TASK = [
        ('PEN', 'В ожидании'),
        ('COM', 'Завершена'),
    ]

    name = models.CharField(
        max_length=255,
        verbose_name='Название задачи'
    )
    description = models.TextField(
        verbose_name='Описание задачи'
    )
    status_task = models.CharField(
        max_length=3,
        choices=STATUS_CHOICES_TASK,
        default='PEN',
        verbose_name='Статус задачи'
    )
    due_date = models.DateTimeField(
        verbose_name='Срок выполнения'
    )
    priority = models.CharField(
        max_length=3,
        choices=PRIORITY_CHOICES,
        default='MID',
        verbose_name='Приоритет задачи'
    )
    manager = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="tasks",
        verbose_name='Ответственный менеджер'
    )
    client = models.ForeignKey(
        to=Client,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="tasks",
        verbose_name='Клиент'
    )
    deal = models.ForeignKey(
        to=Deal,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="tasks",
        verbose_name='Связанная сделка'
    )

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return f'{self.name}'
