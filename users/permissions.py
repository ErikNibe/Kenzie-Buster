from rest_framework import permissions
from rest_framework.views import Request, View
from users.models import User


class IsSelfOrIsEmployee(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: User):
        return obj == request.user or request.user.is_employee
