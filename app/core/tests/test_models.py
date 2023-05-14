"""
Tests for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """Test models."""

    def test_create_username_and_email_successfull(self):
        """Test creating a user with an email is successful."""
        username = 'test'
        email = 'test@example.com'
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
            ['test1', 'test1@EXAMPLE.com', 'test1@example.com'],
            ['test2', 'Test2@Example.com', 'Test2@example.com'],
            ['test3', 'TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4', 'test4@example.COM', 'test4@example.com'],
        ]
        for username, email, expected in sample_emails:
            user = get_user_model().objects.create_user(
                                    username, email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_username_or_email_raises_error(self):
        """Test that creating a user without an
        username or email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                'test', '', 'test123')
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                '', 'test@example.com', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'test',
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
