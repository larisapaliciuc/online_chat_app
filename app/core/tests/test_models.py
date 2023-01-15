"""
Tests for models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model


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
