from rest_framework import serializers

from reviews.models import User


class UserCreateSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
    )
    email = serializers.EmailField(
        max_length=254,
    )

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError('Использовать имя me запрещено.')
        return data


class UserTokenSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )
    confirmation_code = serializers.CharField(
        max_length=150,
        required=True
    )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
