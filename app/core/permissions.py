from .models import Membership, Message
from rest_framework.permissions import BasePermission


class HasReadPermissions(BasePermission):

    def has_permission(self, request, view):
        membership = Membership.objects.all().filter(
            channel=view.kwargs.get('pk'),
            member=request.user
        )
        return True if membership else False


class HasWritePermissions(BasePermission):

    def has_permission(self, request, view):
        membership = Membership.objects.all().filter(
            channel=view.kwargs.get('pk'),
            member=request.user
        )
        if membership:
            return True if membership.permissions >= 2 else False
        return False


class IsMessageOwner(BasePermission):
    message = 'You are not the owner of this message.'

    def has_permission(self, request, view):

        membership = Membership.objects.all().filter(
            channel=view.kwargs.get('pk'),
            member=request.user
        )
        if membership:
            message = Message.objects.all().filter(
                sender=request.user,
                pk=view.kwargs.get('message_id')
            )
            if message:
                return True
        return False
