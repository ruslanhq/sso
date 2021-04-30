from rest_framework import mixins
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from authentication.permission import StaffOnly
from authentication.models import User
from authentication.serializers import (
    UserGroupsSerializer, UserResponseSerializer,
    CustomTokenObtainPairSerializer, UserCreateSerializer
)


class UserViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet
):
    permission_classes = [IsAuthenticated, StaffOnly]
    queryset = User.objects.prefetch_related('groups').filter(is_active=True)

    def get_serializer_class(self):
        if self.action in ['create']:
            return UserCreateSerializer
        elif self.action in ['patch', 'add_to_group', 'destroy']:
            # use for `add_to_group` action
            return UserGroupsSerializer
        else:
            return UserResponseSerializer

    def get_permissions(self):
        if self.action == 'create':
            return []
        elif self.action == 'list':
            return [IsAuthenticated()]
        return super().get_permissions()

    @action(
        methods=['patch'], detail=False, url_name='add_to_group'
    )
    def add_to_group(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        groups = serializer.validated_data['groups']
        user = serializer.validated_data['user_id']
        user.groups.add(*groups)
        return Response({
            'status': True,
            'groups': user.groups.values_list('title', flat=True)
        },
            status=status.HTTP_201_CREATED
        )

    def destroy(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user_id']
        groups = serializer.validated_data['groups']
        user.groups.remove(*groups)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
