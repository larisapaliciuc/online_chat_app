"""
Serializers message API.
"""

from rest_framework import serializers
from core.models import Message


class MessageSerializer(serializers.ModelSerializer):
    """Serializer class for message model."""

    class Meta:

        model = Message
        fields = ['id', 'channel', 'text', 'sender', 'sent_date']
        read_only_fields = ['id', 'sent_date']
