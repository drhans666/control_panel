from django.contrib.auth.models import User

from rest_framework import permissions


class GroupPermission(permissions.BasePermission):

    def has_permission(self, request, view):

        user = User.objects.get(username=request.user)
        group = str(user.groups.all()[0])
        if group == 'hi_user':
            return True
        else:
            return False
