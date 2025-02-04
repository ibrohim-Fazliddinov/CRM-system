from django.contrib.auth import get_user_model
from rest_framework import serializers

from clients.models.client import Client
from users.serializers.nested.serializer_profile import ProfileShortSerializer

User = get_user_model()

class ClientSHortSerializer(serializers.ModelSerializer):
    manager = ProfileShortSerializer()
    class Meta:
        model = Client
        fields = (
            'id',
            'name',
            'email',
            'manager',
            'created_by',
        )