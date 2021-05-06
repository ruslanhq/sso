from rest_framework.generics import mixins
from rest_framework.viewsets import GenericViewSet

from authentication.models import User
from authentication.permission import HeaderPermission
from authentication.serializers import UserResponseSerializer


class UserViewSet(mixins.RetrieveModelMixin, GenericViewSet):
    queryset = User.objects.prefetch_related('groups').filter(is_active=True)
    serializer_class = UserResponseSerializer
    permission_classes = (HeaderPermission,)
