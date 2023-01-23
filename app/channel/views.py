"""
Views for the channel API.
"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Channel
from channel import serializers


class ChannelViewSet(viewsets.ModelViewSet):
    """View for manage channel APIs."""

    serializer_class = serializers.ChannelSerializer
    queryset = Channel.objects.all()

    # api permissions
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve channels an user is member of."""

        return self.queryset.filter(
            members__in=[self.request.user]
        ).order_by('-id')

    def perform_create(self, serializer):
        """Create a new channel."""

        serializer.save(creator=self.request.user)
