"""
Tests for recipe APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Permission, Role

from user.serializers import (
    RoleSerializer,
    PermissionsSerializer,
)


ROLE_URL = reverse('user:role-list')
PERMISSION_URL = reverse('user:permission-list')


def create_role(**params):
    """Create and return a sample role."""
    defaults = {
        'name': 'Sample Role',
    }
    defaults.update(params)

    role = Role.objects.create(**defaults)
    return role


def create_permission(**params):
    """Create and return a sample permission."""
    defaults = {
        'name': 'Sample Permission',
    }
    defaults.update(params)

    permission = Permission.objects.create(**defaults)
    return permission


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicRecipeAPITests(TestCase):
    """Test unathenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(ROLE_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        res_permission = self.client.get(PERMISSION_URL)

        self.assertEqual(res_permission.status_code,
                         status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(
            username='user',
            email='user@example.com',
            password='test123'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_roles(self):
        """Test retrieving a list of roles."""
        create_role()
        create_role()

        res = self.client.get(ROLE_URL)

        roles = Role.objects.all().order_by('id')
        serializer = RoleSerializer(roles, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_role(self):
        """Test creating a recipe."""
        payload = {
            'name': 'Sample role',
        }
        res = self.client.post(ROLE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_retrieve_permission(self):
        """Test retrieving a list of permission."""
        create_permission()
        create_permission()

        res = self.client.get(PERMISSION_URL)

        permission = Permission.objects.all().order_by('id')
        serializer = PermissionsSerializer(permission, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_permission(self):
        """Test creating a permission."""
        payload = {
            'name': 'Sample permission',
        }
        res = self.client.post(PERMISSION_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
