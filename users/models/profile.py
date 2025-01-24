from django.contrib.auth import get_user_model
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from common.models.models import BaseModel


# User = get_user_model()

class Profile(BaseModel):

    user = models.OneToOneField(
        to='users.User',
        related_name='profile',
        on_delete=models.CASCADE,
        verbose_name='Профиль'
    )
    photo = models.ImageField(
        verbose_name='Фото',
        upload_to='users/%Y/%m/%d',
        null=True,
        blank=True,
    )

    phone_number = PhoneNumberField(
        unique=True,
        blank=True,
        verbose_name='Телефон',
        null=True
    )

    class Meta:
        verbose_name = 'Profile'