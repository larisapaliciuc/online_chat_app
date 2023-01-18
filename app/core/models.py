"""
Database models.
"""


from django.utils.translation import gettext as _

from django.conf import settings

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, username, email, password=None, **extra_fields):
        """Create, save and return a new user."""

        if not email:
            raise ValueError('User must have an email address.')
        if not username:
            raise ValueError('User must have an username.')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extra_fields
            )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password):
        """Create and return a new superuser."""

        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


class Channel(models.Model):
    """Channel object."""

    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='creator_of'
    )
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    created_date = models.DateField(auto_now_add=True)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Membership',
        through_fields=('channel', 'member')
    )

    def __str__(self) -> str:
        return str(self.name)


class Membership(models.Model):
    """Membership object."""

    READ = 'R'
    WRITE = 'W'
    ADMIN = 'A'

    PERMISSIONS_CHOICES = [
        (READ, _('Read')),
        (WRITE, _('Write')),
        (ADMIN, _('Admin'))
    ]

    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    inviter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='membership_invites'
    )
    channel = models.ForeignKey(
        Channel,
        on_delete=models.CASCADE,
    )
    permissions = models.CharField(
        max_length=255,
        default=READ,
        choices=PERMISSIONS_CHOICES
    )
    join_date = models.DateField(auto_now_add=True)
