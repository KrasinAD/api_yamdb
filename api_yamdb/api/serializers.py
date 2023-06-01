from rest_framework import serializers

from review.models import CustomUser


class UserCreateSerializer(serializers.ModelSerializer):
    pass


class UserAccessSerializer(serializers.ModelSerializer):
    pass


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )