from django.contrib.auth import get_user_model
from django.db import models
from crum import get_current_user
from django.utils import timezone

User = get_user_model()

class DateMixin(models.Model):

    created_at = models.DateTimeField(
        verbose_name='Создан в',
        blank=True,
    )

    updated_at = models.DateTimeField(
        verbose_name='Обновлен в',
        blank=True,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs) -> None:
        if not self.pk and not self.created_at:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(DateMixin, self).save(*args, **kwargs)

class InfoMixin(DateMixin):

    created_by = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        related_name='created_%(app_label)s_%(class)s',
        verbose_name='Созданный',
        null=True,
    )
    updated_by = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        related_name='updated_%(app_label)s_%(class)s',
        verbose_name='Обновленный',
        null=True,
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs) -> None:
        user = get_current_user()

        if user and not user.pk:
            user = None

        if not self.pk:
            self.created_by = user
        self.updated_by = user
        super().save(*args, **kwargs)