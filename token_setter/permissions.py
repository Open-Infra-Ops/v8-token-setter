from rest_framework import permissions
from django.conf import settings


class QueryPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        token = request.GET.get('token')
        if token and token == settings.CONFIG.get('QUERY_TOKEN'):
            return True
        else:
            return False
