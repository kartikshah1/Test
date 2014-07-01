"""
Views for Discussion Forum
Keeping activity for add operations only. Can be extended easily if required

TODO
    - introduce user specific variable "follow" for thread
        Whether user is following thread or not ?
    - introduce 'liked', variable for Thread/Comment/Reply

    - handle anonymity while serializing thread/comment/reply: instructor \
        can see the User

    - send notification to thread subscriber about new content
"""


from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action, link
from rest_framework.response import Response

from discussion_forum import models
from discussion_forum import permissions
from discussion_forum import serializers

from courseware.models import Concept

ORDER_CHOICES = ['recent', 'earlier', 'popularity']
PAGINATED_BY = 5


@login_required
def forum(request):
    """
    Serves forum.html template
    """
    context = {"request": request}
    return render(request, "discussion_forum/forum.html", context)


@login_required
def forum_admin(request):
    """
    Serves forum.html template
    """
    context = {"request": request}
    return render(request, "discussion_forum/admin.html", context)


def apply_content_filters(order='recent', queryset=None):
    """ Apply sorting_order, disable and pinned filter """
    queryset = queryset.filter(disabled=False)
    if order == 'earlier':
        queryset = queryset.order_by('-pinned', 'created')
    elif order == 'popularity':
        queryset = queryset.order_by('-pinned', '-popularity', '-created')
    else:
        #default order recent
        queryset = queryset.order_by('-pinned', '-created')
    return queryset


def paginated_serializer(request=None, queryset=None, serializer=None):
    """
    Returns the serializer containing objects corresponding to paginated page
    """
    paginator = Paginator(queryset, PAGINATED_BY)
    page = request.QUERY_PARAMS.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        items = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999),
        # deliver last page of results.
        items = paginator.page(paginator.num_pages)
    serializer_context = {'request': request}
    return serializer(items, context=serializer_context)


def get_threads(forum=None, tag=None, request=None, search_term=None):
    """
    Return threads according to the specifications.
    Returns HTTP_400_BAD_REQUEST if any error occurs.
    """
    if tag:
        queryset = models.Thread.objects.filter(tags__pk=tag.pk)
    else:
        queryset = models.Thread.objects.filter(forum=forum)
    if search_term:
        queryset = queryset.filter(content__contains=search_term)
    order = request.QUERY_PARAMS.get('order')
    queryset = apply_content_filters(order=order, queryset=queryset)
    serializer = paginated_serializer(
        request=request,
        queryset=queryset,
        serializer=serializers.PaginatedThreadSerializer
    )
    response = serializer.data
    for result in response["results"]:
        thread = models.Thread.objects.get(pk=result["id"])
        result["subscribed"] = thread.subscription.is_subscribed(request.user)
    return Response(response)


class DiscussionForumViewSet(mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             viewsets.GenericViewSet):
    """
    Methods for this ViewSet. Only retrieve and update are allowed
    """

    model = models.DiscussionForum
    serializer_class = serializers.DiscussionForumSettingSerializer
    permission_classes = [permissions.IsForumAdminOrReadOnly]
    paginate_by = 2

    def retrieve(self, request, pk=None):
        """ Returns discussion_forum object along with tags """
        forum = get_object_or_404(models.DiscussionForum, pk=pk)
        self.check_object_permissions(request, forum)
        print "RETRIEVE CALLED"
        serializer = serializers.DiscussionForumSerializer(forum)
        return Response(serializer.data)

    @action(methods=['POST'], permission_classes=(permissions.IsForumAdmin, ))
    def add_tag(self, request, pk=None):
        """
        Add tag to this DiscussionForum
        """
        forum = get_object_or_404(models.DiscussionForum, pk=pk)
        self.check_object_permissions(request, forum)
        serializer = serializers.ForumTagSerializer(data=request.DATA)
        if serializer.is_valid():
            tag = models.Tag(
                forum=forum,
                title=serializer.data['title'],
                tag_name=serializer.data['tag_name'],
                auto_generated=False
            )
            tag.save()
            return Response(serializers.TagSerializer(tag).data)
        else:
            content = {"detail": "tag-name should be unique across forum-tags"}
            return Response(content, status.HTTP_400_BAD_REQUEST)

    @link(permission_classes=([permissions.IsForumUser]))
    def activity(self, request, pk):
        """
        Returns activities of particular discussion_forum
        """
        forum = get_object_or_404(models.DiscussionForum, pk=pk)
        self.check_object_permissions(request, forum)
        activities = models.Activity.objects.filter(forum=forum)
        activities = activities.order_by('-happened_at')
        serializer = serializers.ActivitySerializer(activities, many=True)
        return Response(serializer.data)

    @link(permission_classes=([permissions.IsForumUser]))
    def user_setting(self, request, pk):
        """
        Returns the user_setting for currently loggedIn user
        """
        forum = get_object_or_404(models.DiscussionForum, pk=pk)
        self.check_object_permissions(request, forum)
        setting = get_object_or_404(
            models.UserSetting,
            forum=forum,
            user=request.user
        )
        serializer = serializers.UserSettingSerializer(setting)
        return Response(serializer.data)

    @link(permission_classes=((permissions.IsForumUser, )))
    def threads(self, request, pk):
        """
        Return list of threads in a particular order
        """
        print "THREAD CLAAED"
        forum = get_object_or_404(models.DiscussionForum, pk=pk)
        self.check_object_permissions(request, forum)
        return get_threads(forum=forum, tag=None, request=request)

    @link(permission_classes=((permissions.IsForumUser, )))
    def search_threads(self, request, pk):
        """
        Return list of threads in a particular order
        """
        search_term = request.GET.get('search', None)
        forum = models.DiscussionForum.objects.get(pk=pk, Content_Forum__content__contains=search_term)
        #forum = get_object_or_404(models.DiscussionForum, pk=pk, Content_Forum__content__contains=search_term)
        self.check_object_permissions(request, forum)
        serializer = serializers.DiscussionForumSerializer(forum)
        return Response(serializer.data)
        return get_threads(forum=forum,
                           tag=None,
                           request=request,
                           search_term=search_term)

    @action(methods=['POST'], permission_classes=((permissions.IsForumUser,)))
    def add_thread(self, request, pk=None):
        """
        Add a new post to the forum
        """
        forum = get_object_or_404(models.DiscussionForum, pk=pk)
        self.check_object_permissions(request, forum)
        serializer = serializers.ForumThreadSerializer(data=request.DATA)
        try:
            user_setting = models.UserSetting.objects.get(
                forum=forum,
                user=request.user
            )
        except:
            content = {'detail': 'Not enough permissions'}
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)
        if serializer.is_valid():
            thread = models.Thread(
                forum=forum,
                author=request.user,
                author_badge=user_setting.badge,
                title=serializer.data['title'],
                content=serializer.data['content'],
                anonymous=serializer.data['anonymous'],
            )
            thread.save()
            forum.thread_count += 1
            forum.save()

            subscribe = serializer.data['subscribe']
            if subscribe:
                thread.subscription.subscribe(request.user)

            models.Activity.activity(
                forum=forum,
                user=request.user,
                operation=models.ActivityOperation.add,
                object_type=models.ActivityObject.thread,
                object_id=thread.pk
            )

            serializer = serializers.ThreadSerializer(thread)
            return Response(serializer.data)
        else:
            content = {"detail": "malformed data"}
            return Response(content, status.HTTP_400_BAD_REQUEST)

    @link(permission_classes=((permissions.IsForumModerator, )))
    def review_content(self, request, pk=None):
        """
        Returns list of disabled content to user
        """
        forum = get_object_or_404(models.DiscussionForum, pk=pk)
        self.check_object_permissions(request, forum)
        content_set = models.Content.objects.filter(forum=forum)
        content_set = content_set.filter(
            Q(spam_count__gt=forum.review_threshold) | Q(disabled=True))
        serializer = paginated_serializer(
            request=request,
            queryset=content_set,
            serializer=serializers.PaginatedContentSerializer
        )
        return Response(serializer.data)

    @link(permission_classes=((permissions.IsForumAdmin, )))
    def users(self, request, pk=None):
        """
        Retuns list of all moderator's UserSetting object
        """
        forum = get_object_or_404(models.DiscussionForum, pk=pk)
        self.check_object_permissions(request, forum)

        queryset = models.UserSetting.objects.filter(forum=forum)

        utype = request.QUERY_PARAMS.get('type')
        if utype == "moderators":
            queryset = queryset.filter(
                Q(super_user=True) | Q(moderator=True)
            )
        elif utype == "search":
            search_str = request.QUERY_PARAMS.get('query')
            queryset = queryset.filter(user__username__icontains=search_str)

        serializer = paginated_serializer(
            request=request,
            queryset=queryset,
            serializer=serializers.PaginatedUserSettingSerializer
        )
        return Response(serializer.data)


class TagViewSet(
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet):
    """
    Methods For this ViewSet
    """

    model = models.Tag
    serializer_class = serializers.TagSerializer
    permission_classes = [permissions.IsForumAdminOrReadOnly]

    # Modified IsForumAdminOrReadOnly permission to restrict admin from \
    # deleting auto_generated tags

    @link(permission_classes=((permissions.IsForumUser, )))
    def threads(self, request, pk=None):
        """ Return list of threads in a particular order """
        tag = get_object_or_404(models.Tag, pk=pk)
        self.check_object_permissions(request, tag)
        return get_threads(forum=tag.forum, tag=tag, request=request)


class UserSettingViewSet(
        mixins.UpdateModelMixin,
        #mixins.DestroyModelMixin,: Automatically deleted on dropping course
        viewsets.GenericViewSet):
    """
    Methods For this ViewSet
    """

    model = models.UserSetting
    serializer_class = serializers.UserSettingSerializer
    permission_classes = [permissions.IsOwnerOrModeratorReadOnly]

    @action(methods=['POST'],
            permission_classes=((permissions.IsForumModerator, )))
    def update_badge(self, request, pk=None):
        """
        Updates badge for a Current User. Only course moderator can update \
        badge
        """
        user_setting = get_object_or_404(models.UserSetting, pk=pk)
        self.check_object_permissions(request, user_setting)

        # Checking for current user's permission
        try:
            current_user_setting = models.UserSetting.objects.get(
                forum=user_setting.forum,
                user=request.user)
        except:
            content = {"detail": "not enough permission"}
            return Response(content, status.HTTP_403_FORBIDDEN)
        if not current_user_setting.moderator:
            content = {"detail": "not enough permission"}
            return Response(content, status.HTTP_403_FORBIDDEN)

        serializer = serializers.BadgeSerializer(data=request.DATA)
        if serializer.is_valid():
            user_setting.badge = serializer.data['badge']
            user_setting.save()
            serializer = serializers.UserSettingSerializer(user_setting)
            return Response(serializer.data)
        else:
            content = {"detail": "malformed data"}
            return Response(content, status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'],
            permission_classes=((permissions.IsForumAdmin, )))
    def update_moderation_permission(self, request, pk=None):
        """
        Update moderator value of UserSetting for this object. Only \
        allowed for Super Usersself.
        """
        user_setting = get_object_or_404(models.UserSetting, pk=pk)
        self.check_object_permissions(request, user_setting)

        # Checking for current user's permission
        try:
            current_user_setting = models.UserSetting.objects.get(
                forum=user_setting.forum,
                user=request.user)
        except:
            content = {"detail": "not enough permission"}
            return Response(content, status.HTTP_403_FORBIDDEN)
        if not current_user_setting.super_user:
            content = {"detail": "not enough permission"}
            return Response(content, status.HTTP_403_FORBIDDEN)

        serializer = serializers.BooleanSerializer(data=request.DATA)
        if serializer.is_valid():
            user_setting.moderator = serializer.data['mark']
            user_setting.save()
            serializer = serializers.UserSettingSerializer(user_setting)
            return Response(serializer.data)
        else:
            content = {"detail": "malformed data"}
            return Response(content, status.HTTP_400_BAD_REQUEST)


class ContentViewSet(mixins.DestroyModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    """
    Methods For this ViewSet
    """

    model = models.Content
    serializer_class = serializers.ContentSerializer
    permission_classes = [permissions.IsOwnerOrModerator]

    def destroy(self, request, pk=None):
        """
        Downcast to appropriate class member and delete that content
        """
        try:
            content = models.Content.objects.get_subclass(id=pk)
            self.check_object_permissions(request, content)
            content.delete()
            response = {"detail": "Content deleted."}
            return Response(response, status=status.HTTP_204_NO_CONTENT)
        except:
            response = {"detail": "invalid delete request"}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @link(permission_classes=((permissions.IsForumUser, )))
    def upvote(self, request, pk=None):
        """
        Do upvote for content object
        """
        content = get_object_or_404(models.Content, pk=pk)
        self.check_object_permissions(request, content)
        content.vote_up(request.user)
        serializer = serializers.ContentSerializer(content)
        return Response(serializer.data)

    @link(permission_classes=((permissions.IsForumUser, )))
    def downvote(self, request, pk=None):
        """
        Do downvote for content object
        """
        content = get_object_or_404(models.Content, pk=pk)
        self.check_object_permissions(request, content)
        content.vote_down(request.user)
        serializer = serializers.ContentSerializer(content)
        return Response(serializer.data)

    @link(permission_classes=((permissions.IsForumUser, )))
    def mark_spam(self, request, pk=None):
        """
        Mark content as spam. If spam count exceeds threshold then content \
        gets disabled
        """
        content = get_object_or_404(models.Content, pk=pk)
        self.check_object_permissions(request, content)
        content.mark_spam(request.user)
        if content.disabled:
            return Response({"detail": "Content is disabled."})
        serializer = serializers.ContentSerializer(content)
        return Response(serializer.data)

    @link(permission_classes=((permissions.IsForumModerator, )))
    def pin_content(self, request, pk=None):
        """
        Pin the content
        """
        content = get_object_or_404(models.Content, pk=pk)
        self.check_object_permissions(request, content)
        content.pinned = not content.pinned
        content.save()
        serializer = serializers.ContentSerializer(content)
        return Response(serializer.data)

    @link(permission_classes=((permissions.IsForumModerator, )))
    def disable(self, request, pk=None):
        """
        Disable the content object
        """
        content = get_object_or_404(models.Content, pk=pk)
        self.check_object_permissions(request, content)
        content.disabled = True
        content.save()
        serializer = serializers.ContentSerializer(content)
        return Response(serializer.data)

    @link(permission_classes=((permissions.IsForumModerator, )))
    def enable(self, request, pk=None):
        """
        Disable the content object
        """
        content = get_object_or_404(models.Content, pk=pk)
        self.check_object_permissions(request, content)
        content.disabled = False
        content.save()
        serializer = serializers.ContentSerializer(content)
        return Response(serializer.data)

    @link(permission_classes=((permissions.IsForumModerator, )))
    def reset_spam_flags(self, request, pk=None):
        """
        Reset spam_count and spammers and enable the content
        """
        content = get_object_or_404(models.Content, pk=pk)
        self.check_object_permissions(request, content)
        content.reset_spam_flags()
        content.disabled = False
        content.save()
        serializer = serializers.ContentSerializer(content)
        return Response(serializer.data)


class ThreadViewSet(
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet):
    """
    Methods For this ViewSet
    """

    model = models.Thread
    serializer_class = serializers.ThreadSerializer
    permission_classes = [permissions.IsOwnerOrModeratorOrReadOnly]

    def retrieve(self, request, pk=None):
        """
        Send a single thread instance. Perform make_hit operation.
        If thread is disabled then it sends HTTP_404_NOT_FOUND
        """
        thread = get_object_or_404(models.Thread, pk=pk)
        self.check_object_permissions(request, thread)
        thread.make_hit()

        if thread.disabled:
            content = {'detail': 'Content is disabled'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializers.ThreadSerializer(thread).data)

    @link(permission_classes=((permissions.IsForumUser, )))
    def comments(self, request, pk=None):
        """
        Returns list of comments
        """
        web_request = request._request
        if 'order' in web_request.GET.keys():
            order = web_request.GET['order']
        else:
            order = 'earlier'
        thread = get_object_or_404(models.Thread, pk=pk)
        self.check_object_permissions(request, thread)
        comments = models.Comment.objects.filter(thread=thread)
        comments = apply_content_filters(queryset=comments, order=order)
        serializer = paginated_serializer(
            request=request,
            queryset=comments,
            serializer=serializers.PaginatedCommentSerializer
        )
        if serializer.data["previous"] is None:
            thread.make_hit()
        return Response(serializer.data)

    @link(permission_classes=((permissions.IsForumUser, )))
    def get_tag_list(self, request, pk=None):
        ## Get all concept Names for this course
        print "PK=", pk
        queryset = Concept.objects.filter(is_published=True).filter(group__course_id=pk)
        data = {}
        print queryset.values()
        data['results'] = queryset.values("id", "title")
        return Response(data)

    @action(methods=['POST'],
            permission_classes=((permissions.IsForumUser, )))
    def add_comment(self, request, pk=None):
        """
        Add a new comment for to the Thread
        """
        thread = get_object_or_404(models.Thread, pk=pk)
        self.check_object_permissions(request, thread)
        serializer = serializers.ForumContentSerializer(data=request.DATA)
        try:
            user_setting = models.UserSetting.objects.get(
                forum=thread.forum,
                user=request.user
            )
        except:
            content = {'detail': 'Not enough permissions'}
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)
        if serializer.is_valid():
            comment = models.Comment(
                thread=thread,
                forum=thread.forum,
                author=request.user,
                author_badge=user_setting.badge,
                content=serializer.data['content'],
                anonymous=serializer.data['anonymous']
            )
            comment.save()
            thread.children_count += 1
            thread.save()

            models.Activity.activity(
                forum=thread.forum,
                user=request.user,
                operation=models.ActivityOperation.add,
                object_type=models.ActivityObject.comment,
                object_id=comment.pk
            )
            return Response(serializers.CommentSerializer(comment).data)
        else:
            content = {"detail": "inconsistent data"}
            return Response(content, status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'],
            permission_classes=((permissions.IsForumUser, )))
    def add_tag(self, request, pk=None):
        """
        Adds a new tag to this thread
        """
        thread = get_object_or_404(models.Thread, pk=pk)
        self.check_object_permissions(request, thread)
        serializer = serializers.IntegerSerializer(data=request.DATA)
        if serializer.is_valid():
            tag_id = serializer.data['value']
            tag = get_object_or_404(models.Tag, pk=tag_id)
            if tag.forum == thread.forum:
                thread.tags.add(tag)
                serializer = serializers.TagSerializer(
                    thread.tags.all(),
                    many=True
                )
                return Response(serializer.data)
            content = {"detail": "un-identified tag"}
            return Response(content, status.HTTP_400_BAD_REQUEST)
        else:
            content = {"detail": "malformed data"}
            return Response(content, status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'],
            permission_classes=((permissions.IsForumUser, )))
    def remove_tag(self, request, pk=None):
        """
        Removes tag from this thread
        """
        thread = get_object_or_404(models.Thread, pk=pk)
        self.check_object_permissions(request, thread)
        serializer = serializers.IntegerSerializer(data=request.DATA)
        if serializer.is_valid():
            tag_id = serializer.data['value']
            tag = get_object_or_404(models.Tag, pk=tag_id)
            if tag.forum == thread.forum:
                thread.tags.remove(tag)
                serializer = serializers.TagSerializer(
                    thread.tags.all(),
                    many=True
                )
                return Response(serializer.data)
            content = {"detail": "un-identified tag"}
            return Response(content, status.HTTP_400_BAD_REQUEST)
        else:
            content = {"detail": "malformed data"}
            return Response(content, status.HTTP_400_BAD_REQUEST)

    @link(permission_classes=((permissions.IsForumUser, )))
    def subscribe(self, request, pk=None):
        """
        Subscribe to this thread notifications
        """
        thread = get_object_or_404(models.Thread, pk=pk)
        self.check_object_permissions(request, thread)
        thread.subscription.subscribe(request.user)
        response = {"success": "your subscribed to thread notifications"}
        response["subscribed"] = True
        return Response(response)

    @link(permission_classes=((permissions.IsForumUser, )))
    def unsubscribe(self, request, pk=None):
        """
        Subscribe to this thread notifications
        """
        thread = get_object_or_404(models.Thread, pk=pk)
        self.check_object_permissions(request, thread)
        thread.subscription.unsubscribe(request.user)
        response = {"success": "you will no longer recieve notifications"}
        response["subscribed"] = False
        return Response(response)


class CommentViewSet(
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet):
    """
    Methods For this ViewSet
    """

    model = models.Comment
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsOwnerOrModeratorOrReadOnly]

    @link(permission_classes=((permissions.IsForumUser, )))
    def replies(self, request, pk=None):
        """
        Returns list of replies in discussion_forum
        """
        web_request = request._request
        if 'order' in web_request.GET.keys():
            order = web_request.GET['order']
        else:
            order = 'earlier'
        comment = get_object_or_404(models.Comment, pk=pk)
        self.check_object_permissions(request, comment)
        replies = models.Reply.objects.filter(comment=comment)
        replies = apply_content_filters(queryset=replies, order=order)
        serializer = paginated_serializer(
            request=request,
            queryset=replies,
            serializer=serializers.PaginatedReplySerializer
        )
        return Response(serializer.data)

    @action(methods=['POST'],
            permission_classes=((permissions.IsForumUser, )))
    def add_reply(self, request, pk=None):
        """
        Add a new reply for to the comment
        """
        comment = get_object_or_404(models.Comment, pk=pk)
        self.check_object_permissions(request, comment)
        serializer = serializers.ForumContentSerializer(data=request.DATA)
        try:
            user_setting = models.UserSetting.objects.get(
                forum=comment.forum,
                user=request.user
            )
        except:
            content = {'detail': 'Not enough permissions'}
            return Response(content, status=status.HTTP_401_UNAUTHORIZED)
        if serializer.is_valid():
            reply = models.Reply(
                thread=comment.thread,
                comment=comment,
                forum=comment.forum,
                author=request.user,
                author_badge=user_setting.badge,
                content=serializer.data['content'],
                anonymous=serializer.data['anonymous']
            )
            reply.save()
            comment.children_count += 1
            comment.save()

            models.Activity.activity(
                forum=comment.forum,
                user=request.user,
                operation=models.ActivityOperation.add,
                object_type=models.ActivityObject.reply,
                object_id=reply.pk
            )
            return Response(serializers.ReplySerializer(reply).data)
        else:
            content = {"detail": "inconsistent data"}
            return Response(content, status.HTTP_400_BAD_REQUEST)


class ReplyViewSet(
        mixins.RetrieveModelMixin,
        mixins.UpdateModelMixin,
        mixins.DestroyModelMixin,
        viewsets.GenericViewSet):
    """
    Reply ViewSet.
    Allowed methods are retrieve, content update and delete
    """

    model = models.Reply
    serializer_class = serializers.ReplySerializer
    permission_classes = [permissions.IsOwnerOrModeratorOrReadOnly]
