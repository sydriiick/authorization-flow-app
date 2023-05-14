"""
URL mapping for the user API.
"""
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from user import views


router_users = DefaultRouter()
router_users.register('users', views.ManageUserView)

router_role = DefaultRouter()
router_role.register('roles', views.RoleViewSet)

router_permissions = DefaultRouter()
router_permissions.register('permissions', views.PermissionViewSet)


app_name = 'user'


urlpatterns = [
    path('', include(router_users.urls)),
    path('', include(router_role.urls)),
    path('', include(router_permissions.urls)),
    path('signup/', views.CreateUserView.as_view(), name='create'),
    path('login/', views.CreateTokenView.as_view(), name='token'),
]
