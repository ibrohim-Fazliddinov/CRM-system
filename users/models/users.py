from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from common.models.manager import CustomUserManager
from users.models.profile import Profile


class User(AbstractUser):

    class Role(models.TextChoices):
        """"""
        ADMIN = 'ADM', _('Администратор')
        MANAGER = 'MNG', _('Менеджер'),
        CUSTOMER = 'CUS', _('Клиент')

    username = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Никнейм'
    )

    first_name = models.CharField(
        max_length=45,
        verbose_name='Имя'
    )

    last_name = models.CharField(
        max_length=45,
        verbose_name='Фамилия'
    )

    email = models.EmailField(
        unique=True,
        verbose_name='Почта'
    )

    phone_number = None

    role = models.CharField(
        max_length=3,
        choices=Role.choices,
        default=Role.CUSTOMER,
        verbose_name='Роль'
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()


    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_full_name(self) -> str:
        return f'{self.first_name} | {self.last_name}'

    def __str__(self) -> str:
        return f'{self.username} | {self.email}'



@receiver(post_save, sender=User)
def post_save_user(sender, instance: User, created, **kwargs)-> None:
    if not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)