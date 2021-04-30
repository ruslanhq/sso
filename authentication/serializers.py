from rest_framework import serializers
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from authentication.fields import RPCEndpointField
from authentication.models import User, Groups


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(many=True, slug_field='title',
                                          queryset=Groups.objects.all())

    class Meta:
        model = User
        fields = ('email', 'username', 'groups',)


class UserGroupsSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_active=True)
    )
    groups = serializers.SlugRelatedField(
        many=True, slug_field='title',
        queryset=Groups.objects.filter(is_active=True)
    )

    class Meta:
        model = User
        fields = ('user_id', 'groups',)


class UserResponseSerializer(serializers.Serializer):
    user = UserSerializer(read_only=True, source='*')
    endpoint = RPCEndpointField(read_only=True, source='*')
    http_status = serializers.IntegerField(default=status.HTTP_200_OK)


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password',)
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        return token
