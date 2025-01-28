from rest_framework import serializers
from clients.models.deals import Deal


class TaskList(serializers.ModelSerializer):
    class Meta:
        model = Deal
        fields = '__all__'