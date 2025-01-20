from __future__ import annotations
from typing import TYPE_CHECKING
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views.auth import CustomTokenObtainPairView, CustomTokenRefreshView, CustomTokenVerifyView
from users.views.users import AuthView, PasswordChangingView

if TYPE_CHECKING:
    from django.urls.resolvers import URLPattern


def filter_routes(urls: list[URLPattern], allowed_patterns: tuple[str, ...]) -> list[URLPattern]:
    """
    Фильтрация маршрутов: оставляет только URL-адреса, содержащие шаблоны из списка разрешенных.

    :param urls: Список URL-адресов для фильтрации.
    :param allowed_patterns: Кортеж шаблонов для разрешения.
    :return: Отфильтрованный список URL-адресов.
    """
    filtered_urls = []
    for url in urls:
        if any(pattern in url.pattern.describe() for pattern in allowed_patterns):
            filtered_urls.append(url)
    return filtered_urls

# Настройка маршрутов
router = DefaultRouter()
router.register(r'auth', AuthView, basename='auth')
router.register(r'password', PasswordChangingView, basename='password')

# Разрешенные URL-шаблоны
allowed_urls = (
    'password/change_password/',
    'password/reset_password/',
    'password/reset_password_confirm/',

    'auth/activate/',
    'auth/registration/',
    'auth/user_list/',
    'auth/user_search/',
    'auth/user_update/',
)

# Фильтруем маршруты пользователей
filtered_user_routes = filter_routes(router.urls, allowed_urls)

# Основные маршруты
urlpatterns = [
    path('auth/jwt/create', CustomTokenObtainPairView.as_view(), name='create-token'),
    path('auth/jwt/refresh', CustomTokenRefreshView.as_view(), name='refresh-token'),
    path('auth/jwt/verify', CustomTokenVerifyView.as_view(), name='verify-token'),
    *filtered_user_routes,  # Распаковка отфильтрованных маршрутов
]
