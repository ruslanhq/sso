from rest_framework import serializers
from rest_framework import status

from authentication.fields import RPCEndpointField
from authentication.models import User, Groups


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(many=True, slug_field='title',
                                          queryset=Groups.objects.all())

    class Meta:
        model = User
        fields = ('email', 'username', 'groups',)


class UserGroupsSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(many=True, slug_field='title',
                                          queryset=Groups.objects.all())

    class Meta:
        model = User
        fields = ('groups',)


class UserResponseSerializer(serializers.Serializer):
    user = UserSerializer(read_only=True, source='*')
    endpoint = RPCEndpointField(read_only=True, source='*')
    http_status = serializers.IntegerField(default=status.HTTP_200_OK)
