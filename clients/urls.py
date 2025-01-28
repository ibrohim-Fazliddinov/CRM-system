from __future__ import annotations

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from clients.viewa.client import ClientView
from clients.viewa.deal import DealCreateView

router = DefaultRouter()
router.register(r'client', ClientView, 'client')
router.register(r'deals', DealCreateView, 'deal')




urlpatterns = [
    path('', include(router.urls)),
    # path('deals/', DealCreateView.as_view(), name='deal'),
]

