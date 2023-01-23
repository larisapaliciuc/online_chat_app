"""
Tests for models.
"""
from django.db import IntegrityError
from datetime import date
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating user with an email is successful."""
        username = 'exampleuser'
        email = "test@example.com"
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        self.assertEqual(user.username, username)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test@EXAMPLE.com', 'test@example.com'],
            ['Test1@Example.com', 'Test1@example.com'],
            ['TEST2@EXAMPLE.COM', 'TEST2@example.com'],
            ['test3@example.COM', 'test3@example.com'],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(
                f'sample_{email}',
                email,
                'sample123'
                )
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating user without an email raises ValueError."""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                'user_no_email',
                '',
                'test123'
                )

    def test_new_user_without_username_raises_error(self):
        """Test that creating user without an email raises a ValueError."""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                '',
                'emailsample@example.com',
                'test123'
                )

    def test_create_superuser(self):
        """Test creating a superuser."""

        user = get_user_model().objects.create_superuser(
            'admin',
            'adminuser@example.com',
            'admpas'
        )

        self.assertEqual(user.username, 'admin')
        self.assertEqual(user.email, 'adminuser@example.com')
        self.assertTrue(user.check_password('admpas'))
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_channel_successful(self):
        """Test creating a channel is successful."""

        creator = get_user_model().objects.create(
            username='channel_creator',
            email='test@example.com',
            password='pas123'
        )

        channel = models.Channel.objects.create(
            name='Channel Test',
            description='Channel description',
            creator=creator,
        )

        self.assertEqual(str(channel), channel.name)
        self.assertEqual(channel.created_date, date.today())

    def test_create_channel_adds_creator_as_member(self):
        """Test creating a channel adds the creator as member."""

        creator = get_user_model().objects.create(
            username='channel_creator',
            email='test@example.com',
            password='pas123'
        )

        channel = models.Channel.objects.create(
            name='Channel Test',
            description='Channel description',
            creator=creator,
        )

        membership = models.Membership.objects.filter(channel=channel)[0]

        self.assertEqual(str(channel), channel.name)
        self.assertEqual(membership.permissions, 'A')
        self.assertTrue(creator in channel.members.all())
        self.assertEqual(channel.created_date, date.today())

    def test_create_duplicate_channel_name_fails(self):
        """Tests creating 2 channels with same name fails."""

        creator = get_user_model().objects.create(
            username='channel_creator',
            email='test@example.com',
            password='pas123'
        )

        models.Channel.objects.create(
            name='Channel Test',
            description='Channel description',
            creator=creator,
        )

        with self.assertRaises(IntegrityError):
            models.Channel.objects.create(
                name='Channel Test',
                description='Channel description 1',
                creator=creator,
            )

    def test_create_membership_successful(self):
        """Test creating a membership"""

        inviter = get_user_model().objects.create(
            username='inviter_user',
            email='inviter@email.com',
            password='inv123'
        )
        member = get_user_model().objects.create(
            username='member_user',
            email='member@email.com',
            password='mem123'
        )
        channel = models.Channel.objects.create(
            creator=inviter,
            name='Channel Test',
            description='Description test'
        )
        membership = models.Membership.objects.create(
            inviter=inviter,
            member=member,
            channel=channel
        )

        self.assertEqual(membership.join_date, date.today())
        self.assertEqual(membership.channel.name, channel.name)

    def test_channel_memberships(self):
        """Test that a channel can have multiple memberships."""

        inviter = get_user_model().objects.create(
            username='inviter_user',
            email='inviter@email.com',
            password='inv123'
        )
        channel = models.Channel.objects.create(
            creator=inviter,
            name='Channel Test',
            description='Description test'
        )
        member1 = get_user_model().objects.create(
            username='member1_user',
            email='member1@email.com',
            password='mem123'
        )
        member2 = get_user_model().objects.create(
            username='member2_user',
            email='member2@email.com',
            password='mem1234'
        )
        models.Membership.objects.create(
            inviter=inviter,
            member=member1,
            channel=channel
        )
        models.Membership.objects.create(
            inviter=inviter,
            member=member2,
            channel=channel
        )

        self.assertEqual(len(channel.members.all()), 3)
        self.assertTrue(member2 in channel.members.all())
        self.assertTrue(member1 in channel.members.all())

    def test_default_mermbership_permissions(self):
        """Tests membership permissions."""

        inviter = get_user_model().objects.create(
            username='inviter_user',
            email='inviter@email.com',
            password='inv123'
        )
        channel = models.Channel.objects.create(
            creator=inviter,
            name='Channel Test',
            description='Description test'
        )
        member = get_user_model().objects.create(
            username='member_user',
            email='member@email.com',
            password='mem123'
        )
        membership = models.Membership.objects.create(
            inviter=inviter,
            member=member,
            channel=channel
        )

        self.assertEqual(membership.get_permissions_display(), 'Read')

    def test_set_membership_permissions_successful(self):
        """Tests membership permissions are correctly set."""

        inviter = get_user_model().objects.create(
            username='inviter_user',
            email='inviter@email.com',
            password='inv123'
        )
        channel = models.Channel.objects.create(
            creator=inviter,
            name='Channel Test',
            description='Description test'
        )
        member = get_user_model().objects.create(
            username='member_user',
            email='member@email.com',
            password='mem123'
        )
        membership = models.Membership.objects.create(
            inviter=inviter,
            member=member,
            channel=channel,
            permissions='A'
        )

        self.assertEqual(membership.get_permissions_display(), 'Admin')

    def test_message_created_successfully(self):
        """Test a message is created successfully"""

        sender = get_user_model().objects.create(
            username='Sender User',
            email='sender@example.com',
            password='mypassword'
        )
        channel = models.Channel.objects.create(
            creator=sender,
            name='Channel',
            description='My channel'
        )
        text = 'Hello! My name is Larisa. 😍'

        message = models.Message.objects.create(
            sender=sender,
            channel=channel,
            text=text
        )

        self.assertEqual(message.sent_date, date.today())
        self.assertEqual(message.channel, channel)
        self.assertEqual(str(message), text)
