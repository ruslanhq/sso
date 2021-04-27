from rest_framework import fields


class RPCEndpointField(fields.URLField):
    def to_representation(self, _):
        return self.context['request'].build_absolute_uri()
