""""
Handles permission for Discussion Forum API management
To access any record of a forum User must be part of that forum

Permission Classes:
    IsForumAdminOrReadOnly
    - safe methods allowed for all forum users. other actions for admin only

    IsOwnerOrModeratorReadOnly
    - owner has full access while moderator has just read access. False for \
      others

    IsOwnerOrModerator
    - owner and moderator has full access rest have none access

    IsOwnerOrModeratorOrReadOnly
    - owner and moderator has full access rest have read only access

    IsForumAdmin
    - Checks for forum admin

    IsForumModerator
    - Checks for forum moderator+admin

    IsForumUser
    - Checks whether loggedIn user is subscribed to forum or not

DiscussionForum:
    + retrieve: IsForumAdminOrReadOnly
    + patching: partial update: IsForumAdminOrReadOnly
    - add_tag: IsForumAdmin
    - activity: IsForumUser
    - threads: IsForumUser
    - add_thread: IsForumUser
    - review_content: IsForumModerator

Tag: forum:
    + retrieve: IsForumAdminOrReadOnly
    + patching: partial update: IsForumAdminOrReadOnly
    + delete: IsForumAdminOrReadOnly
    - threads: IsForumUser

UserSetting: forum
    + retrieve: IsOwnerOrModeratorReadOnly
    + patching: partial update: IsOwnerOrModeratorReadOnly
    - update_badge: IsForumModerator
    - update_moderation_permission: IsForumAdmin

Content: forum
    + delete: IsOwnerOrModerator
    - upvote, downvote, mark_spam: IsForumUser
    - pin_content: IsForumModerator
    - disable: IsForumModerator
    - enable: IsForumModerator
    - reset_spam_flags: IsForumModerator

Thread: forum
    + retrieve: IsOwnerOrModeratorOrReadOnly
    + update: IsOwnerOrModeratorOrReadOnly
    + delete: IsOwnerOrModeratorOrReadOnly
    - comments: ForumUser
    - add_comment: ForumUser
    - add_tag: ForumUser
    - remove_tag: ForumUser
    - subscribe: ForumUser
    - unsubscribe: ForumUser
Comment: forum
    + retrieve: IsOwnerOrModeratorOrReadOnly
    + update: IsOwnerOrModeratorOrReadOnly
    + delete: IsOwnerOrModeratorOrReadOnly
    - replies: IsForumUser
    - add_reply: IsForumUser
Reply: forum
    + retrieve: IsOwnerOrModeratorOrReadOnly
    + update: IsOwnerOrModeratorOrReadOnly
    + delete: IsOwnerOrModeratorOrReadOnly
"""


from rest_framework import permissions

from discussion_forum import models


class IsForumAdminOrReadOnly(permissions.BasePermission):
    """
    Allows complete permission to Forum Admin and read only access to other \
    forum users
    """

    def has_permission(self, request, view):
        """
        Allow loggedIn users only
        """
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        """
        Returns whehter user has permission on this object or not
        """
        try:
            if type(obj) == models.DiscussionForum:
                forum = obj
            else:
                forum = obj.forum
            setting = models.UserSetting.objects.get(
                forum=forum,
                user=request.user
            )
        except:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            if type(obj) == models.Tag and obj.auto_generated:
                # Auto generated tags can't be operated on
                return False
            return setting.super_user


class IsOwnerOrModeratorReadOnly(permissions.BasePermission):
    """
    Complete access to owner and read only access to moderator. Other's have \
    no access at all
    """

    def has_permission(self, request, view):
        """
        Allow loggedIn users only
        """
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        """
        Returns whehter user has permission on this object or not
        """
        try:
            if type(obj) == models.DiscussionForum:
                forum = obj
            else:
                forum = obj.forum

            if type(obj) == models.UserSetting:
                owner = obj.user
            else:
                owner = obj.author

            setting = models.UserSetting.objects.get(
                forum=forum,
                user=request.user
            )
        except:
            return False

        if request.method in permissions.SAFE_METHODS:
            if setting.super_user or setting.moderator:
                return True
            else:
                return owner == request.user
        else:
            return (owner == request.user)


class IsOwnerOrModerator(permissions.BasePermission):
    """
    Owner and Moderator have full access other's have no access at all
    """

    def has_permission(self, request, view):
        """
        Allow loggedIn users only
        """
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        """
        Returns whehter user has permission on this object or not
        """
        try:
            if type(obj) == models.DiscussionForum:
                forum = obj
            else:
                forum = obj.forum

            if type(obj) == models.UserSetting:
                owner = obj.user
            else:
                owner = obj.author

            setting = models.UserSetting.objects.get(
                forum=forum,
                user=request.user
            )
        except:
            return False

        if (setting.super_user or setting.moderator):
            return True
        else:
            return (owner == request.user)


class IsOwnerOrModeratorOrReadOnly(permissions.BasePermission):
    """
    Full access to owner and moderator. Other forum users have Readonly access
    """

    def has_permission(self, request, view):
        """
        Allow loggedIn users only
        """
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        """
        Returns whehter user has permission on this object or not
        """
        try:
            if type(obj) == models.DiscussionForum:
                forum = obj
            else:
                forum = obj.forum

            if type(obj) == models.UserSetting:
                owner = obj.user
            else:
                owner = obj.author

            setting = models.UserSetting.objects.get(
                forum=forum,
                user=request.user
            )
        except:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True
        elif (setting.super_user or setting.moderator):
            return True
        else:
            return (owner == request.user)


class IsForumAdmin(permissions.BasePermission):
    """
    Provide access for moderation purpose to Forum Super User's only
    """

    def has_permission(self, request, view):
        """
        Allow loggedIn users only
        """
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        """
        Check for forum admin
        """
        try:
            if type(obj) == models.DiscussionForum:
                forum = obj
            else:
                forum = obj.forum

            setting = models.UserSetting.objects.get(
                forum=forum,
                user=request.user
            )
        except:
            return False
        return setting.super_user


class IsForumModerator(permissions.BasePermission):
    """
    Provide access for moderation purpose to Forum Moderators
    """

    def has_permission(self, request, view):
        """
        Allow loggedIn users only
        """
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        """
        Check for forum moderator
        """
        try:
            if type(obj) == models.DiscussionForum:
                forum = obj
            else:
                forum = obj.forum

            setting = models.UserSetting.objects.get(
                forum=forum,
                user=request.user
            )
        except:
            return False
        return (setting.super_user or setting.moderator)


class IsForumUser(permissions.BasePermission):
    """
    General permission class for ForumUser
    """

    def has_permission(self, request, view):
        """
        Allow loggedIn users only
        """
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        """
        Check whether current user is subscribed to forum or not
        """
        try:
            if type(obj) == models.DiscussionForum:
                forum = obj
            else:
                forum = obj.forum

            setting = models.UserSetting.objects.get(
                forum=forum,
                user=request.user
            )
        except:
            return False
        return True
