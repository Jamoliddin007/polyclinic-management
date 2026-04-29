"""
Rollarga asoslangan permission'lar.

Rollar (Django Group nomlari):
  - admin       — to'liq ruxsat
  - registrator — bemorlar, murojaatlar, to'lovlar (read+write)
  - doctor      — o'z murojaatlarini tahrirlash, tashxis kiritish
"""
from rest_framework.permissions import BasePermission, SAFE_METHODS


def in_group(user, group_name: str) -> bool:
    return user.is_authenticated and (
        user.is_superuser or user.groups.filter(name=group_name).exists()
    )


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return in_group(request.user, 'admin')


class IsRegistrator(BasePermission):
    def has_permission(self, request, view):
        return in_group(request.user, 'registrator') or in_group(request.user, 'admin')


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return in_group(request.user, 'doctor') or in_group(request.user, 'admin')


class IsAdminOrReadOnly(BasePermission):
    """Admin yoza oladi, qolganlar faqat o'qiy oladi."""
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return in_group(request.user, 'admin')


class IsAdminOrRegistratorOrReadOnly(BasePermission):
    """Admin/registrator yoza oladi, doctor faqat o'qiy oladi."""
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated
        return in_group(request.user, 'admin') or in_group(request.user, 'registrator')
