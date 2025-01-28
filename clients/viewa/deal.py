from typing import Any

from django.db import transaction
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from clients.models.deals import Deal
from clients.serializers.api.deal import DealCreateSerializer, DealListSerializer, DealUpdateSerializer, \
    DealDeleteSerializer
from common.views import CLUDViewSet, CreateViewSet


@extend_schema_view(
    deal_create=extend_schema(
        summary='create', tags=['---']
    ),
)
class DealCreateView(CreateViewSet):
    queryset = Deal.objects.all()
    serializer_class = DealCreateSerializer
    http_method_names = ('post','get')

    def perform_create(self, serializer):
        # Автоматически устанавливаем текущего пользователя как менеджера
        serializer.save(manager=self.request.user)