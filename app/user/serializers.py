"""
Serializers for the user API View.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _

from rest_framework import serializers

from core.models import User, Role, UserRole, Permission


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user objects."""

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}
                        }

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        user = get_user_model().objects.create_user(**validated_data)
        UserRole.objects.create(user=user)
        return user

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        password = attrs.get('password')

        username = User.objects.filter(email=attrs.get("username")).first()
        email = User.objects.filter(username=attrs.get("username")).first()

        user_obj = username or email

        user = authenticate(
            request=self.context.get('request'),
            username=user_obj.email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class PermissionsSerializer(serializers.ModelSerializer):
    """Serializer for Permission."""

    class Meta:
        model = Permission
        fields = ['id', 'name']
        read_only_fields = ['id']


class RoleSerializer(serializers.ModelSerializer):
    """Serializers for Role."""
    permissions = PermissionsSerializer(many=True, required=False)

    class Meta:
        model = Role
        fields = ['id', 'name', 'permissions']
        read_only_fields = ['id']

    def _get_permissions(self, permissions, role):
        """Handle getting permission as needed."""
        for permission in permissions:
            permission_obj = Permission.objects.get(
                **permission,
            )
            role.permissions.add(permission_obj)

    def create(self, validated_data):
        """Create a role."""
        permissions = validated_data.pop('permissions', [])
        role = Role.objects.create(**validated_data)
        self._get_permissions(permissions, role)
        return role

    def update(self, instance, validated_data):
        """Update role."""
        permissions = validated_data.pop('permissions', None)
        if permissions is not None:
            instance.permissions.clear()
            self._get_permissions(permissions, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        return instance


class UserRoleSerializer(serializers.ModelSerializer):
    """Serializers for user-roles."""
    roles = RoleSerializer(many=True, required=False)

    class Meta:
        model = UserRole
        fields = ['id', 'user', 'roles']
        read_only_fields = ['id', 'user']

    def update(self, instance, validated_data):
        """Update user-roles."""
        roles = validated_data.pop('roles', None)
        if roles is not None:
            instance.roles.clear()
            for role in roles:
                role_obj = Role.objects.get(
                    **role
                )
                instance.roles.add(role_obj)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
