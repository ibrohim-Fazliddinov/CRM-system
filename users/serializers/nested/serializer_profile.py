from rest_framework import serializers
from users.models.profile import Profile


class ProfileShortSerializer(serializers.ModelSerializer):
    """Вложенный сериализатор профиля"""

    class Meta:
        model = Profile
        fields = (
            'photo',
            'phone_number',
        )

class ProfileUpdateSerializer(serializers.ModelSerializer):
    """Вложенный сериализатор обновления профиля"""

    class Meta:
        model = Profile
        fields = (
            'photo',
            'phone_number',
        )
