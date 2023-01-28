"""Serializers for channels API.
"""

from core.models import Channel
from rest_framework import serializers


class ChannelSerializer(serializers.ModelSerializer):
    """Serializer for channels."""

    class Meta:
        model = Channel
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']
