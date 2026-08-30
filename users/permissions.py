from rest_framework import permissions

class IsOwnerOrModerator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        user = request.user
        if user.is_staff:
            return True
        if hasattr(user, "groups") and user.groups.filter(name="moders").exists():
            return True
        return False
