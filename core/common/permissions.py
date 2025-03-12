from rest_framework import permissions
from core.general.models import CustomUser

class BaseUserTypePermission(permissions.BasePermission):
    user_type = None

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == self.user_type


class IsAdmin(BaseUserTypePermission):
    user_type = CustomUser.Positions.ADMIN


class IsDoctor(BaseUserTypePermission):
    user_type = CustomUser.Positions.DOCTOR


class IsExpert(BaseUserTypePermission):
    user_type = CustomUser.Positions.EXPERT


class IsReceptionist(BaseUserTypePermission):
    user_type = CustomUser.Positions.RECEPTIONIST


class IsNurse(BaseUserTypePermission):
    user_type = CustomUser.Positions.NURSE


class IsAccountant(BaseUserTypePermission):
    user_type = CustomUser.Positions.ACCOUNTANT


class IsCollaborator(BaseUserTypePermission):
    user_type = CustomUser.Positions.COLLABORATOR


class IsEmployee(BaseUserTypePermission):
    user_type = CustomUser.Positions.EMPLOYEE
