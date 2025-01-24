from django.urls import path, include
from rest_framework.routers import DefaultRouter
from common.utils import filter_routes
from users.views.auth import CustomTokenObtainPairView, CustomTokenRefreshView, CustomTokenVerifyView
from users.views.users import AuthView, PasswordChangingView


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
