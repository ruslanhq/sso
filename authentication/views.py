from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins

from authentication.models import User
from authentication.serializers import UserSerializer


class UserViewSet(mixins.RetrieveModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all().prefetch_related('groups')
