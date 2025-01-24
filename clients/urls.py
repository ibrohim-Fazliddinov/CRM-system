from __future__ import annotations

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from clients.views import ClientView

router = DefaultRouter()
router.register(r'client', ClientView, 'client')




urlpatterns = [
    path('', include(router.urls))
]

