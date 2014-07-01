"""
Handles permissions of the courseware API

Permission Classes:
    IsInstructorOrReadOnly
    - safe methods allowed for all users. other only for instructor

    IsContentDeveloper
    - Checks whether he is a ContentDeveloper

    IsRegistered
    - Checks whether the student is enrolled in the course
"""

from rest_framework import permissions
from courseware.models import CourseHistory
from user_profile.models import CustomUser
from courseware.models import Group, Concept


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    safe methods allowed for all the users. other only for admin
    """
    def has_permission(self, request, view):
        """
        Returns whether user has permission for this table or not
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        """
        Returns whether user has permission on this object or not
        """
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_superuser


class IsContentDeveloperOrReadOnly(permissions.BasePermission):
    """
        Check if the current mode of operation is valid
        and in content developer mode
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if request.user.is_authenticated():
                customuser = CustomUser.objects.get(user=request.user)
                if customuser.is_content_developer:
                    return True
            return False

    def has_object_permission(self, request, view, obj):
        """
        Returns whether user has permission on this object or not
        """
        if request.user.is_authenticated():
            # return true if he is the content developer for this textbook
            try:
                CourseHistory.objects.get(
                    course=obj,
                    user=request.user,
                    is_owner=True
                )
            except:
                if request.method in permissions.SAFE_METHODS:
                    # return true if he is an instructor
                    customuser = CustomUser.objects.get(user=request.user)
                    if customuser.is_instructor:
                        return True
                return False
            return True
        return False


class IsInstructorOrReadOnly(permissions.BasePermission):
    """
    Allows complete permission to instructor and list access to others
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if request.user.is_authenticated():
                customuser = CustomUser.objects.get(user=request.user)
                if customuser.is_instructor:
                    return True
            return False

    def has_object_permission(self, request, view, obj):
        """
        Returns whether user has permission on this object or not
        """
        if request.user.is_authenticated():
            if request.method in permissions.SAFE_METHODS:
                # return true if registered
                try:
                    CourseHistory.objects.get(
                        course=obj,
                        user=request.user,
                        active='A'
                    )
                except:
                    return False
                return True

            # return true if he is the instructor for this offering
            try:
                CourseHistory.objects.get(
                    course=obj,
                    user=request.user,
                    is_owner=True
                )
            except:
                return False
            return True
        return False


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Allows complete permission to the owner and list access to others
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if request.user.is_authenticated():
                customuser = CustomUser.objects.get(user=request.user)
                if customuser.is_instructor or customuser.is_content_developer:
                    return True
            return False

    def has_object_permission(self, request, view, obj):
        """
        Returns whether user has permission on this object or not
        """
        if request.user.is_authenticated():
            if type(obj) == Group:
                obj = obj.course
            if type(obj) == Concept:
                obj = obj.group.course
            if request.method in permissions.SAFE_METHODS:
                # return true if registered if it is an offering
                if obj.type == 'O':
                    try:
                        CourseHistory.objects.get(
                            course=obj,
                            user=request.user,
                            active='A'
                        )
                    except:
                        return False
                    return True
                elif obj.type == 'T':
                    customuser = CustomUser.objects.get(user=request.user)
                    if customuser.is_instructor:
                        return True
                return False

            # return true if he is the owner of the course
            try:
                CourseHistory.objects.get(
                    course=obj,
                    user=request.user,
                    is_owner=True
                )
            except:
                return False
            return True
        return False


class IsOwner(permissions.BasePermission):
    """
    Allows complete permission to the owner and none to others
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated():
            customuser = CustomUser.objects.get(user=request.user)
            if customuser.is_instructor or customuser.is_content_developer:
                return True
        return False

    def has_object_permission(self, request, view, obj):
        """
        Returns whether user has permission on this object or not
        """
        if request.user.is_authenticated():
            # return true if he is the owner of the course
            try:
                CourseHistory.objects.get(
                    course=obj,
                    user=request.user,
                    is_owner=True
                )
            except:
                return False
            return True
        return False


class IsRegistered(permissions.BasePermission):
    """Checks whether a user is registered in the course"""
    def has_permission(self, request, view):
        """
        Checks whether person is the course instructor or is a superuser
        """
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        try:
            if request.user.is_authenticated():
                CourseHistory.objects.get(
                    course=obj,
                    user=request.user,
                    active='A')
            else:
                return False
        except:
            return False
        return True
