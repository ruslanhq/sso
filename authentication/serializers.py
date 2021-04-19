from rest_framework import serializers

from authentication.models import User


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'groups',)
