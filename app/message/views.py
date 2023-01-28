"""
Views for message API.
"""

from rest_framework import (
    viewsets,
    mixins
)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from message import serializers
from core.models import Message


class MessageViewSet(mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    """Viewset class for message API."""

    serializer_class = serializers.MessageSerializer
    queryset = Message.objects.all()

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    http_method_names = ["patch"]
