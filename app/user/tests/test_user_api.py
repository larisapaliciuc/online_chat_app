"""Test for user API."""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    """Create and return new user."""

    return get_user_model().objects.create_user(**params)


class PublicUserAPITests(TestCase):
    """Test the public features of the user API."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test creating a user is successful."""

        payload = {
            'password': 'borna12345',
            'username': 'borna',
            'email': 'borna@example.com',
            'name': 'Test Borna',
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(username=payload['username'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_username_exists_email(self):
        """Test error returned if user with username exists."""

        payload = {
            'username': 'test_user',
            'email':    'testuser@example.com',
            'name': 'Test Name',
        }

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Tests an error is returned if password less than 8 chars."""

        payload = {
            'email': 'testuser@example.com',
            'password': 'pwd',
            'name': 'Test Name',
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def create_test_token_for_user(self):
        """Generates token for valid credentials."""

        user_details = {
            'password': 'borna12345',
            'username': 'borna',
            'email': 'borna@example.com',
            'name': 'Test Borna',
        }
        create_user(**user_details)

        payload = {
            'email': user_details('email'),
            'password': user_details('password'),
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test return error if credentials invalid."""

        create_user(
            username='testuser',
            password='goodpas',
            email='test@example.com'
        )

        payload = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'badpassword',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Tests posting a blank password return an error."""

        payload = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': '',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
