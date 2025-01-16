from typing import Optional, Union
from django.contrib.auth.base_user import BaseUserManager
from rest_framework.exceptions import ParseError


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create(
            self,
            email: [Optional] = None,
            username: [Optional] = None,
            password: [Optional] = None,
            **extra_fields: Optional[str]
    ):
        if not (username or email):
            raise ParseError("Укажите свою почту или Никнейм")

        if email:
            email = self.normalize_email(email)

        if not username:
            username = email.split('@')[0]

        user = self.model(username=username, **extra_fields)
        if email:
            user.email = email
        if user.is_superuser:
            user.role = user.Role.ADMIN

        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(
            self,
            email: [Optional] = None,
            username: [Optional] = None,
            password: [Optional] = None,
            **extra_fields: Union[str, bool]
    ):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_active', False)

        return self._create(email, username, password, **extra_fields)

    def create_superuser(
            self,
            email: [Optional] = None,
            username: [Optional] = None,
            password: [Optional] = None,
            **extra_fields: Union[str, bool]
    ):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self._create(email, username, password, **extra_fields)


