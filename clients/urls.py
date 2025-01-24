from __future__ import annotations
from rest_framework.routers import DefaultRouter
from clients.views import ClientView
from common.utils import filter_routes

router = DefaultRouter()
router.register(r'client', ClientView, 'client')
# Разрешенные URL-шаблоны
allowed_urls = (
    'client/client_create/',
    'client/client_list/',
    'client/client_update/',
    'client/search/',
)


# Фильтруем маршруты пользователей
filtered_routes = filter_routes(router.urls, allowed_urls)
urlpatterns = [
    *filtered_routes
]

