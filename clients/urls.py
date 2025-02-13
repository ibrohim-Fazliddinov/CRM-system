from __future__ import annotations
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from clients.viewa.client import ClientView
from clients.viewa.deal import DealView
from clients.viewa.task import TaskView

router = DefaultRouter()
router.register(r'clients', ClientView, 'client')
router.register(r'deals', DealView, 'deal')
router.register('tasks', TaskView, 'tasks')



urlpatterns = [
    path('', include(router.urls)),
]

