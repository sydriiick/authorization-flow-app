"""
Views for the user API.
"""
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework import (
    viewsets,
)
from rest_framework import (
    generics,
    authentication,
    permissions,
    status
)
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
    RoleSerializer,
    UserRoleSerializer,
    PermissionsSerializer
)

from core.models import User, Role, UserRole, Permission


class CreateUserView(generics.CreateAPIView):
    """Create a nuew user in the systems."""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(viewsets.ModelViewSet):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['put', 'get']

    @action(detail=True, methods=['get', 'put'])
    def roles(self, request, pk=None):
        """Adding and getting roles to user."""
        if request.method == 'PUT':
            queryset = UserRole.objects.all()
            user_role = get_object_or_404(queryset, user=pk)
            serializer = UserRoleSerializer(instance=user_role,
                                            data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                roles = serializer.data['roles']
                for role in roles:
                    role.pop("permissions", None)
                return Response(roles, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'GET':
            queryset = UserRole.objects.all()
            user_role = get_object_or_404(queryset, user=pk)
            serializer = UserRoleSerializer(instance=user_role, many=False)
            roles = serializer.data['roles']
            for role in roles:
                role.pop("permissions", None)
            return Response(roles, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def permissions(self, request, pk=None):
        """Listing all the permissions of user."""
        queryset = UserRole.objects.all()
        user_role = get_object_or_404(queryset, user=pk)
        serializers = UserRoleSerializer(instance=user_role, many=False)
        roles = serializers.data['roles']
        for role in roles:
            role.pop("name", None)
        return Response(roles, status=status.HTTP_200_OK)


class RoleViewSet(viewsets.ModelViewSet):
    """View for manage roles APIs."""
    serializer_class = RoleSerializer
    queryset = Role.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['put', 'get', 'post']

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return RoleSerializer

        return self.serializer_class

    @action(detail=True, methods=['get', 'put'])
    def permissions(self, request, pk=None):
        """Adding and getting permissions to role."""
        if request.method == 'PUT':
            queryset = Role.objects.all()
            role = get_object_or_404(queryset, pk=pk)
            serializer = RoleSerializer(instance=role,
                                        data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data,
                                status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'GET':
            queryset = Role.objects.all()
            role = get_object_or_404(queryset, pk=pk)
            serializer = RoleSerializer(instance=role, many=False)
            return Response(serializer.data,
                            status=status.HTTP_200_OK)


class PermissionViewSet(viewsets.ModelViewSet):
    """View for manage permissions APIs."""
    serializer_class = PermissionsSerializer
    queryset = Permission.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['put', 'get', 'post']

    def perform_create(self, serializer):
        """Create a new permission."""
        serializer.save()
