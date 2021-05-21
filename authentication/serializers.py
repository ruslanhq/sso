from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework import status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from authentication.fields import RPCEndpointField
from authentication.models import User, Groups, EcomInformation


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(
        many=True, slug_field='title', queryset=Groups.objects.all()
    )

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
        return User.objects.create_user(**validated_data)


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                {"old_password": "Old password is not correct"}
            )
        return value

    def save(self, **kwargs):
        password = self.validated_data['password']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user


class EcomInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EcomInformation
        exclude = ('id',)

    def create(self, validated_data):
        user = self.context['request'].user
        ecom_info = EcomInformation.objects.create(**validated_data)
        user.company = ecom_info
        user.save()
        return ecom_info


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['username'] = user.username
        return token
