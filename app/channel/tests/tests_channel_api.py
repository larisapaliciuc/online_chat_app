"""
Tests for channel API
"""

from datetime import date

from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Channel,
    Message,
)

from channel.serializers import ChannelSerializer

CHANNELS_URL = reverse('channel:channel-list')
MESS_URL = 'channel:channel-messages'
PATCH_MSG_URL = 'channel:channel-patch-messages'


def create_channel(creator, **params):
    """Create and return a sample channel."""

    defaults = {
        'name': 'Sample Channel',
        'description': 'Sample description',
    }

    defaults.update(params)

    channel = Channel.objects.create(creator=creator, **defaults)

    return channel


def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create(**params)


class PublicChannelAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""

        res = self.client.get(CHANNELS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateChannelsAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            username='User',
            email='email@example.com',
            password='pass123'
        )
        self.client.force_authenticate(self.user)

    def test_recieve_channels(self):
        """Test receiving a list of channels a user is member of."""

        create_channel(creator=self.user)
        create_channel(creator=self.user, name='Channel2')

        res = self.client.get(CHANNELS_URL)

        channels = Channel.objects.filter(
            members__in=[self.user]
        ).order_by('-id')
        serializer = ChannelSerializer(channels, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_channels_limited_to_user(self):
        """Test list of channels is limited to authenticated user."""

        other_user = create_user(
            username='User2',
            email='email1@example.com',
            password='pas123'
        )

        create_channel(creator=self.user)
        create_channel(creator=other_user, name='ChannelUser2')

        res = self.client.get(CHANNELS_URL)

        channels = Channel.objects.filter(members__in=[self.user])
        serializer = ChannelSerializer(channels, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_channel(self):
        """Test creating a channel through the API."""

        payload = {
            'name': 'Sample channel',
            'description': 'Sample description'
        }

        res = self.client.post(CHANNELS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        channel = Channel.objects.get(id=res.data['id'])

        for k, v in payload.items():
            self.assertEqual(getattr(channel, k), v)
        self.assertEqual(channel.creator, self.user)

    def test_partial_update(self):
        """Test partial update of channel."""

        original_description = "Original description"
        channel = create_channel(
            creator=self.user,
            name='Channel Old Name',
            description=original_description
        )

        payload = {'name': 'New Channel Name'}
        id = channel.id
        url = reverse('channel:channel-detail', args=[id])
        res = self.client.patch(url, payload)
        channel.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(channel.name, payload['name'])
        self.assertEqual(channel.description, original_description)
        self.assertEqual(channel.creator, self.user)
        self.assertEqual(channel.created_date, date.today())

    def test_full_update(self):
        """Test full update of channel."""

        channel = create_channel(
            creator=self.user,
            name='Channel Old Name',
            description="Description"
        )
        payload = {
            'name': 'New Channel Name',
            'description': 'New description'
        }

        url = reverse('channel:channel-detail', args=[channel.id])
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        channel.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(channel, k), v)
        self.assertEqual(channel.creator, self.user)

    def test_update_creator_returns_error(self):
        """Test update of creator returns error"""

        channel = create_channel(
            creator=self.user,
            name='Channel Old Name',
            description="Description"
        )

        other_user = create_user(
            username='User2',
            email='email1@example.com',
            password='pas123'
        )

        payload = {
            'creator': other_user
        }

        url = reverse('channel:channel-detail', args=[channel.id])
        self.client.patch(url, payload)
        channel.refresh_from_db()
        self.assertEqual(channel.creator, self.user)

    def test_delete_channel(self):
        """Test delete channel successfully"""

        channel = create_channel(
            creator=self.user,
            name='Channel',
            description='Description'
        )

        url = reverse('channel:channel-detail', args=[channel.id])
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Channel.objects.filter(id=channel.id).exists())

    def test_delete_channel_other_users_channel_error(self):
        """Test trying to delete another user's channel returns error."""

        new_user = create_user(
            username='User2',
            email='email1@example.com',
            password='pas123'
        )

        channel = create_channel(
            creator=new_user,
            name='Channel',
            description='Description'
        )

        url = reverse('channel:channel-detail', args=[channel.id])
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Channel.objects.filter(id=channel.id).exists())

    def test_list_channel_messages_successful(self):
        """Test listing messages of a channel is successful."""

        channel = Channel.objects.create(
            creator=self.user,
            name='Channel',
            description='My channel'
        )
        text = 'Hello! My name is Larisa. 😍'

        message = Message.objects.create(
            sender=self.user,
            channel=channel,
            text=text
        )

        res = self.client.get(reverse(MESS_URL, args=[channel.id]))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(message.sender, self.user)
        self.assertEqual(len(res.data), 1)

    def test_update_your_message_channel(self):
        """Test updating your message from a channel."""

        payload = {'text': 'Hello! My name also includes Paliciuc.'}

        channel = Channel.objects.create(
            creator=self.user,
            name='Channel',
            description='My channel'
        )

        message = Message.objects.create(
            sender=self.user,
            channel=channel,
            text='Hello! My name is Larisa. 😍'
        )

        url = reverse(
            PATCH_MSG_URL,
            kwargs={
                'message_id': message.id,
                'pk': channel.id
                }
            )

        res = self.client.patch(url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        message.refresh_from_db()
        self.assertEqual(message.text, payload['text'])

    def test_update_somebody_else_message_channel(self):
        """Test updating a message from a channel not sent by you."""

        payload = {'text': 'Hello! My name also includes Paliciuc.'}

        sender = get_user_model().objects.create(
            username='Sender User',
            email='sender@example.com',
            password='mypassword'
        )
        channel = Channel.objects.create(
            creator=sender,
            name='Channel',
            description='My channel'
        )

        message = Message.objects.create(
            sender=sender,
            channel=channel,
            text='Hello! My name is Larisa. 😍'
        )

        url = reverse(
            PATCH_MSG_URL,
            kwargs={
                'message_id': message.id,
                'pk': channel.id
                }
            )

        res = self.client.patch(url, payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
