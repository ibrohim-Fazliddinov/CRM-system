from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework_simplejwt import views

@extend_schema_view(
    post=extend_schema(
        summary='Создание Токена',
        tags=['🔑 Токены для Аутентификации']
    )
)
class CustomTokenObtainPairView(views.TokenObtainPairView):
    """Представление для создания токена"""
    pass


@extend_schema_view(
    post=extend_schema(
        summary='Обновление Токена',
        tags=['🔑 Токены для Аутентификации']
    )
)
class CustomTokenRefreshView(views.TokenRefreshView):
    """Представление для обновления токена"""
    pass


@extend_schema_view(
    post=extend_schema(
        summary='Проверка Токена',
        tags=['🔑 Токены для Аутентификации']
    )
)
class CustomTokenVerifyView(views.TokenVerifyView):
    """Представление проверки токена"""
    pass

