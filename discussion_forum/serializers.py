"""
Serializer classes for Django Rest Framework
"""

from django.contrib.auth.models import User
from rest_framework import serializers, pagination

from discussion_forum import models


class ForumTagSerializer(serializers.Serializer):
    """ Serializer for parsing Tag attribtues while creating new Tag """
    title = serializers.CharField(max_length=models.SHORT_TEXT)
    tag_name = serializers.CharField(max_length=models.SHORT_TEXT)


class ForumThreadSerializer(serializers.Serializer):
    """ Serializer class for Parsing Thread attributes while creating """
    title = serializers.CharField(max_length=models.SHORT_TEXT)
    content = serializers.CharField()
    anonymous = serializers.BooleanField()
    subscribe = serializers.BooleanField()  # Post and subscribe


class BooleanSerializer(serializers.Serializer):
    """ Serializer class for BooleanField """
    mark = serializers.BooleanField(required=True)


class OrderSerializer(serializers.Serializer):
    """ Serializer for sort order """
    order = serializers.CharField()


class IntegerSerializer(serializers.Serializer):
    """ Serializer class for IntegerField """
    value = serializers.IntegerField(required=True)


class BadgeSerializer(serializers.Serializer):
    """ Serialzer class for Badge """
    badge = serializers.CharField(max_length=2)


class ForumContentSerializer(serializers.Serializer):
    """ Content Serializer while creating new one """
    content = serializers.CharField()
    anonymous = serializers.BooleanField()


class UserSerializer(serializers.ModelSerializer):
    """ Serializer for django.contrib.auth.User """
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class TagSerializer(serializers.ModelSerializer):
    """ serialization for Tag modal """
    class Meta:

        """ Meta """
        model = models.Tag

    def restore_object(self, attrs, instance=None):
        """ Updates tag's title or discussion_models."""
        if instance:
            # Update existing instance
            instance.title = attrs.get('title', instance.title)
            instance.tag_name = attrs.get('tag_name', instance.tag_name)
            return instance
        else:
            return None


class DiscussionForumSerializer(serializers.ModelSerializer):
    """ serialization for DiscussionForum modal """
    tags = TagSerializer(many=True)

    class Meta:
        """ Meta """
        model = models.DiscussionForum

    def restore_object(self, attrs, instance=None):
        """ Updates DiscussionForum object """
        if instance:
            # Update existing instance
            instance.abuse_threshold = attrs.get(
                'abuse_threshold',
                instance.abuse_threshold
            )
            instance.review_threshold = attrs.get(
                'review_threshold',
                instance.review_threshold
            )
            return instance
        else:
            return None


class DiscussionForumSettingSerializer(serializers.ModelSerializer):
    """ serialization for DiscussionForum modal without tags """

    class Meta:
        """ Meta """
        model = models.DiscussionForum


class UserSettingSerializer(serializers.ModelSerializer):
    """ serialization for UserSetting modal """
    user = UserSerializer()

    class Meta:
        """ Meta """
        model = models.UserSetting

    def restore_object(self, attrs, instance=None):
        """ This can only update email_setting """
        if instance:
            instance.email_digest = attrs.get(
                'email_digest',
                instance.email_digest
            )
            return instance
        else:
            return None


class PaginatedUserSettingSerializer(pagination.PaginationSerializer):
    """ Serializing UserSetting class as a list """
    class Meta:
        """ Meta """
        object_serializer_class = UserSettingSerializer


class ActivitySerializer(serializers.ModelSerializer):
    """ serialization for Activity modal """
    actor = UserSerializer()

    class Meta:
        """ Meta """
        model = models.Activity


class ContentSerializer(serializers.ModelSerializer):
    """ serialization for Content modal """
    author = serializers.Field(source='get_author')

    class Meta:
        """ Meta """
        model = models.Content
        # Need to exclude author if anonymous is true
        exclude = ("spammers", "old_spammers", "upvoters", "downvoters")

    def restore_object(self, attrs, instance=None):
        """ Can only update content attribute """
        if instance:
            instance.content = attrs.get('content', instance.content)
            return instance
        else:
            return None


class PaginatedContentSerializer(pagination.PaginationSerializer):
    """
    Serializers page objects of Comment queryset
    """
    class Meta:
        """ Meta """
        object_serializer_class = ContentSerializer


class ThreadListSerializer(serializers.ModelSerializer):
    """ Serializing thread class leaving some attributes for efficiency """
    class Meta:
        model = models.Thread
        exclude = ("spammers", "old_spammers",
                   "upvoters", "downvoters",
                   "subscription", "tags", "author")


class ThreadSerializer(serializers.ModelSerializer):
    """ serialization for Thread modal """
    tags = TagSerializer(many=True)
    author = serializers.Field(source='get_author')

    class Meta:
        """ Meta """
        model = models.Thread
        exclude = ("spammers", "old_spammers",
                   "upvoters", "downvoters",
                   "subscription")

    def restore_object(self, attrs, instance=None):
        """ Can only update thread's title or content """
        if instance:
            instance.title = attrs.get('title', instance.title)
            instance.content = attrs.get('content', instance.content)
            return instance
        else:
            return None


class PaginatedThreadSerializer(pagination.PaginationSerializer):
    """
    Serializers page objects of Thread queryset
    """
    class Meta:
        """ Meta """
        object_serializer_class = ThreadSerializer


class CommentSerializer(serializers.ModelSerializer):
    """ serialization for Comment modal """
    author = serializers.Field(source='get_author')

    class Meta:
        """ Meta """
        model = models.Comment
        exclude = ("spammers", "old_spammers", "upvoters", "downvoters")

    def restore_object(self, attrs, instance=None):
        """ Can only update comment's content """
        if instance:
            instance.content = attrs.get('content', instance.content)
            return instance
        else:
            return None


class PaginatedCommentSerializer(pagination.PaginationSerializer):
    """
    Serializers page objects of Comment queryset
    """
    class Meta:
        """ Meta """
        object_serializer_class = CommentSerializer


class ReplySerializer(serializers.ModelSerializer):
    """ serialization for Reply modal """
    author = serializers.Field(source='get_author')

    class Meta:
        """ Meta """
        model = models.Reply
        exclude = ("spammers", "old_spammers", "upvoters", "downvoters")

    def restore_object(self, attrs, instance=None):
        """ Can only update reply's content """
        if instance:
            instance.content = attrs.get('content', instance.content)
            return instance
        else:
            return None


class PaginatedReplySerializer(pagination.PaginationSerializer):
    """
    Serializers page objects of Thread queryset
    """
    class Meta:
        """ Meta """
        object_serializer_class = ReplySerializer


class NotificationSerializer(serializers.ModelSerializer):
    """ serialization for Reply modal """
    class Meta:
        """ Meta """
        model = models.Notification
