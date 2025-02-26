from rest_framework import serializers


class AnalyticsSerializer(serializers.Serializer):
    deals_by_status = serializers.DictField()
    monthly_income = serializers.DictField()