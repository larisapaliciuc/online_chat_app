"""
Views for the channel API.
"""

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


from core.models import (
    Channel,
    Message,
)
from core.permissions import (
    HasReadPermissions,
    HasWritePermissions,
    IsMessageOwner
)

from channel import serializers
from message.serializers import MessageSerializer


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

    @action(
        methods=['get'],
        detail=True,
        permission_classes=[IsAuthenticated, HasReadPermissions],
        serializer_class=MessageSerializer
    )
    def messages(self, request, pk=None):
        """View for messages app."""
        queryset = Message.objects.all().filter(channel=pk).order_by('id')
        context = {
            'request': request
        }
        serializer = MessageSerializer(queryset, many=True, context=context)
        return Response(serializer.data)

    @action(
        methods=['post'],
        detail=True,
        permission_classes=[IsAuthenticated, HasWritePermissions],
        serializer_class=MessageSerializer,
        url_path='messages'
    )
    def post_messages(self, request, pk=None):
        request.data['channel'] = pk
        request.data['sender'] = request.user.id

        serializer = MessageSerializer(data=request.data)

        if serializer.is_valid():
            Message.objects.create(**serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        methods=['patch'],
        detail=True,
        permission_classes=[IsAuthenticated, IsMessageOwner],
        serializer_class=MessageSerializer,
        url_path=r'messages/(?P<message_id>\d+)'
    )
    def patch_messages(self, request, pk=None, message_id=None):

        request.data['id'] = message_id
        request.data['channel'] = pk
        msg_obj = Message.objects.get(pk=message_id)
        serializer = MessageSerializer(
            msg_obj,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
