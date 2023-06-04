from rest_framework import serializers
from django.db import models

from review.models import User


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username')


class UserAccessSerializer(serializers.Serializer):

    username = models.CharField(
        max_length=150,
        unique=True,
    ),

    confirmation_code = ()



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )