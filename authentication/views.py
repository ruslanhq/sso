from rest_framework import mixins
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from authentication.models import User, Groups
from authentication.serializers import (
    UserSerializer, UserGroupsSerializer, UserResponseSerializer
)


class UserViewSet(
    mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
    mixins.CreateModelMixin, GenericViewSet
):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.prefetch_related('groups').filter(is_active=True)

    def get_serializer_class(self):
        if self.action in ['retrieve']:
            return UserResponseSerializer
        elif self.action in ['patch', 'add_to_group']:
            # use for `add_to_group` action
            return UserGroupsSerializer
        else:
            return UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return []
        return super().get_permissions()

    @action(
        methods=['patch'], detail=False, url_name='add_to_group'
    )
    def add_to_group(self, request):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        groups = serializer.validated_data['groups']
        group = Groups.objects.filter(title__in=groups, is_active=True)
        user.groups.add(*group)
        return Response({
            'status': True,
            'groups': user.groups.values_list('title', flat=True)
        },
            status=status.HTTP_201_CREATED
        )

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserGroupsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        group = Groups.objects.filter(
            title__in=serializer.validated_data['groups']
        )
        user.groups.remove(*group)
        return Response(status=status.HTTP_204_NO_CONTENT)
