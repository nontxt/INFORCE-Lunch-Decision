from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Allows access only to owner and superuser users.
    """

    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve', 'get_menu']:
            return True

        return bool(request.user.groups.filter(name='Owner').exists() or request.user.is_superuser)


class IsEmployee(BasePermission):
    """
    Allows access only to employee and superuser users.
    """

    def has_permission(self, request, view):
        if view.action in ['vote', 'unvote']:
            return bool(request.user.groups.filter(name='Employee').exists() or request.user.is_superuser)

        return True
