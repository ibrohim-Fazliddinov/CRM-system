from django.contrib.auth import get_user_model
from rest_framework import serializers

from clients.models.client import Client

User = get_user_model()
