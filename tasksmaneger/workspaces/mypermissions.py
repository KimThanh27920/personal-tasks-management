from rest_framework import permissions
from rest_framework.response import Response
from .models import Workspace
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.user == request.user

class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if obj.user == request.user or request.user.is_superuser:
            return True
       
class IsSuperUser(permissions.BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)



class IsOwnerWorkspace(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            owner = Workspace.objects.get(id=view.kwargs['workspace_id'])
        except:
            return False
        return request.user == owner.user