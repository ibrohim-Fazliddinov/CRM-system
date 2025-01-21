from django.contrib.auth import get_user_model
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework.exceptions import ValidationError

User= get_user_model()

class Client(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя')
    email = models.EmailField(unique=True, verbose_name='Электронная почта')
    phone_number = PhoneNumberField(
        null=True,
        blank=True,
        verbose_name='Номер телефона'
    )

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
        limit_choices_to={'role': 'MNG'},
    )
    is_active = models.BooleanField(default=True, verbose_name='Активный клиент')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return f'{self.name}|{self.email}'

    # def save(self, *args, **kwargs):
    #     if self.manager.clients.count() >= MAX_CLIENTS_PER_MANAGER:
    #         raise ValidationError(f'Менеджер {self.manager} не может иметь больше {MAX_CLIENTS_PER_MANAGER} клиентов.')
    #     super().save(*args, **kwargs)
