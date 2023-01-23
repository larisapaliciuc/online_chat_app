"""Serializers for channels API.
"""

from rest_framework import serializers

from core.models import Channel


class ChannelSerializer(serializers.ModelSerializer):
    """Serializer for channels."""

    class Meta:
        model = Channel
        fields = ['id', 'name', 'creator', 'description']
        read_only_fields = ['id', 'creator']
