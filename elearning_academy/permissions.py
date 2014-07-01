"""
    Handles the mode of User and associated permissions
"""

from rest_framework import permissions
from user_profile.models import CustomUser


class InInstructorMode(permissions.BasePermission):
    """
        Check if the current mode of operation is valid
        and in instructor mode
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated():
            if 'mode' in request.session:
                customuser = CustomUser.objects.get(user=request.user)
                if request.session['mode'] == 'I' and customuser.is_instructor:
                    return True
            else:
                request.session['mode'] = 'S'
        return False


class InContentDeveloperMode(permissions.BasePermission):
    """
        Check if the current mode of operation is valid
        and in content developer mode
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated():
            if 'mode' in request.session:
                customuser = CustomUser.objects.get(user=request.user)
                if (request.session['mode'] == 'C' and customuser.is_content_developer):
                    return True
            else:
                request.session['mode'] = 'S'
        return False


class InInstructorOrContentDeveloperMode(permissions.BasePermission):
    """
        Check if the current mode of operation is valid
        and in either instructor or content developer mode
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated():
            if 'mode' in request.session:
                customuser = CustomUser.objects.get(user=request.user)
                if request.session['mode'] == 'C':
                    if customuser.is_content_developer:
                        return True
                elif request.session['mode'] == 'I':
                    if customuser.is_instructor:
                        return True
            else:
                request.session['mode'] = 'S'
        return False


def is_valid_mode(request):
    """
        Check if the current mode is valid for this user
    """
    if request.user.is_authenticated():
        if 'mode' in request.session:
            if request.session['mode'] == 'S':
                return True
            customuser = CustomUser.objects.get(user=request.user)
            if request.session['mode'] == 'C':
                if customuser.is_content_developer:
                    return True
            elif request.session['mode'] == 'I':
                if customuser.is_instructor:
                    return True
        else:
            request.session['mode'] = 'S'
    return False


def get_mode(request):
    """
        Return the mode if the mode is valid otherwise returns False
    """
    if request.user.is_authenticated():
        if (is_valid_mode(request)):
            return request.session['mode']
    return False
