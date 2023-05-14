"""
Tests for the user API.
"""
import json
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Role, UserRole


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
USER_URL = reverse('user:user-list')


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


def create_userroles(**params):
    """Create and return a new user."""
    return UserRole.objects.create(**params)


def create_roles(**params):
    """Create and return a new user."""
    return Role.objects.create(**params)


class PublicUserApiTests(TestCase):
    """Test the public features of the user API."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            username='test',
            email='test@example.com',
            password='test123'
        )
        self.client.force_authenticate(self.user)

    def test_create_user_success(self):
        """Test creating a user is successful."""
        payload = {
            'username': 'test1',
            'email': 'test1@example.com',
            'password': 'test123!',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        username = get_user_model().objects.get(username=payload['username'])
        self.assertTrue(username.check_password(payload['password']))
        email = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(email.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_user_exists_error(self):
        """Test error returned if user with email exists."""
        payload = {
            'username': 'test1',
            'email': 'test1@example.com',
            'password': 'testpass123',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_for_user(self):
        """Test generates token for valid credentials."""
        user_details = {
            'username': 'test1',
            'email': 'test1@example.com',
            'password': 'test-user-password123',
        }
        create_user(**user_details)

        payload = {
            'username': user_details['username'],
            'password': user_details['password'],
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test returns error if credentials invalid."""
        create_user(
            username='test1',
            email='test1@example.com',
            password='goodpass'
        )

        payload = {
            'username': 'test1',
            'email': 'test1@example.com',
            'password': 'badpass'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error."""
        payload = {
            'username': 'test@example.com',
            'password': ' '
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            username='test',
            email='test@example.com',
            password='testpass123',
        )
        self.client.force_authenticate(user=self.user)

        self.role = Role.objects.create(
            name='Sample Role',
        )

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user."""
        res = self.client.get(USER_URL, pk=1)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(dict(res.data[0]), {
            'username': self.user.username,
            'email': self.user.email,
        })

    def test_add_and_get_roles(self):
        """Test adding and getting roles"""

        create_userroles(user=self.user)

        payload = {'roles': [{'name': 'Sample Role'}]}

        res_put = self.client.put(
            reverse('user:user-roles', args=[self.user.id]),
            payload,
            format='json'
        )
        self.assertEqual(res_put.status_code, status.HTTP_200_OK)

        res_get = self.client.get(
            reverse('user:user-roles', args=[self.user.id]),
            payload,
            format='json'
        )
        res = json.loads(json.dumps(res_get.data))[0]
        self.assertEqual(res['name'], payload['roles'][0]['name'])
