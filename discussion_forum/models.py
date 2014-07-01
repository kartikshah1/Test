"""
    Contains overall database schema for Discussion Forum
"""

#from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from model_utils.managers import InheritanceManager

from util.models import HitCounter, TimeKeeper, Subscription


# Length for CharField
SHORT_TEXT = 255
LONG_TEXT = 1023

BADGE_CHOICES = (
    ('CT', 'Course Staff'),
    ('IN', 'Instructor'),
    ('MO', 'Moderator'),
    ('ST', 'Student'),
    ('TA', 'Teaching Assistant'),
    ('AN', 'Anonymous')
)


class ActivityOperation:
    """ Meta attributes for Activity.operation """
    add = "add"
    delete = "delete"
    edit = "edit"
    update = "update"
    upvote = "upvote"
    downvote = "downvote"
    spam = "spam"


class ActivityObject:
    """ Meta attributes for Activity.object_type """
    thread = "thread"
    comment = "comment"
    reply = "reply"


def get_user_info(user):
    """ Returns user information in dictionary object """
    ret = {"username": user.username}
    ret["first_name"] = user.first_name
    ret["last_name"] = user.last_name
    ret["id"] = user.pk
    return ret


class DiscussionForum(TimeKeeper):
    """
    Main root object for a particular discussion forum.
    Each offering/course will have OneToOne relationship with \
    this forum object
    """

    thread_count = models.IntegerField(default=0)
    abuse_threshold = models.IntegerField(
        default=5,
        help_text="Maximum abuse count after which content will be \
            marked as Spam"
    )
    review_threshold = models.IntegerField(
        default=2,
        help_text="Abuse count after which content will be displayed for \
            moderator's review"
    )

    def tags(self):
        """ Returns all tags associated with self """
        return list(Tag.objects.filter(forum=self))

    def register(self, user):
        """ Register user for the forum if user is not enrolled """
        obj, created = UserSetting.objects.get_or_create(forum=self, user=user)
        obj.save()

    def unregister(self, user):
        """ UnRegister user from the current forum """
        obj, created = UserSetting.objects.get_or_create(forum=self, user=user)
        obj.delete()


class Tag(models.Model):
    """ Tag corresponding to a forum """

    forum = models.ForeignKey(DiscussionForum, related_name='Forum_Tag')
    title = models.CharField(
        max_length=SHORT_TEXT,
        help_text="Title for Tag for display. Should be unique for Course"
    )
    tag_name = models.CharField(
        max_length=SHORT_TEXT,
        help_text="Alias for above title in lowercase satisfying \
        regular_expression='[a-z0-9_-]+.' Should be unique for Course"
    )

    # This is to distinguish tags which are generated by Admin and the ones
    # which are generated automatically.
    # auto_generated tags can't be deleted or modified by admin
    auto_generated = models.BooleanField(default=True)

    # Each Learning Element will have a OneToOne relationship with this
    # Class and forum will be same as of corresponding Course/Offering

    class Meta:  # pylint: disable=W0232, C0111
        unique_together = ("forum", "tag_name")


class UserSetting(TimeKeeper):
    """
    This class stores user settings for a particular Forum
    """

    user = models.ForeignKey(User, related_name="UserSetting_User")
    forum = models.ForeignKey(
        DiscussionForum,
        related_name="UserSetting_Forum"
    )

    # To check whether the user is still registered in the forum or not
    is_active = models.BooleanField(default=True)

    # Email subscription for daily forum activity
    email_digest = models.BooleanField(default=True)

    # Provide administration privileges. Can make changes on moderator \
    # user control and
    super_user = models.BooleanField(default=False)

    # Moderation privileges over forum. Can delete post/comment
    moderator = models.BooleanField(default=False)

    # Current badge of user will be embedded with content generated by user
    badge = models.CharField(
        max_length=2,
        choices=BADGE_CHOICES,
        default='ST'
    )

    class Meta:
        """ Specifying index and primary key property """
        unique_together = ('user', 'forum')
        index_together = [
            ['user', 'forum'],
        ]


class Activity(models.Model):
    """
    Stores activity of forum. Aimed to retrieve the activity happened in a \
    particular time period
    """

    forum = models.ForeignKey(
        DiscussionForum,
        db_index=True,
        related_name="forum_activity"
    )

    actor = models.ForeignKey(
        User,
        db_index=True,
        related_name='user_activity'
    )

    happened_at = models.DateTimeField(auto_now_add=True, db_index=True)
    operation = models.CharField(max_length=32)  # add/delete/like/edit
    object_type = models.CharField(max_length=32)  # post/thread/reply
    object_id = models.IntegerField(default=0)  # primary key of object

    @staticmethod
    def activity(
            forum=None,
            user=None,
            operation=None,
            object_type=None,
            object_id=None):
        """ Generate a new activity record """
        act = Activity(
            forum=forum,
            actor=user,
            operation=operation,
            object_type=object_type,
            object_id=object_id
        )
        act.save()

    # TODO: Function for activity of specified time till now
    # TODO: Wrapper function for activity of last day, week and month


class Content(TimeKeeper, HitCounter):
    """
    Abstracted class used for storing common content related information \
    generated by user

    Votable Functionality included within for performance issues
    """

    forum = models.ForeignKey(DiscussionForum, related_name="Content_Forum")
    author = models.ForeignKey(User, related_name="Content_User")

    children_count = models.IntegerField(default=0)

    # The badge of author at the creation time of this content. Badge of \
    # author may change but this will remain same
    author_badge = models.CharField(max_length=2, choices=BADGE_CHOICES)

    content = models.TextField()
    pinned = models.BooleanField(default=False)  # Only moderator has access
    anonymous = models.BooleanField(default=False)  # Posted as Anonymous ?

    # If many people mark this content as Spam then content will be disabled\
    # and will be listed for moderator's action
    disabled = models.BooleanField(default=False)

    spam_count = models.IntegerField(default=0)

    # Indexed for efficient sorting on colum
    upvotes = models.IntegerField(default=0, db_index=True)
    downvotes = models.IntegerField(default=0, db_index=True)

    # upvotes-downvotes
    popularity = models.IntegerField(default=0, db_index=True)

    # Helps in selecting subclasses directly
    objects = InheritanceManager()

    class Meta:
        """ Meta attributes for this class """
        abstract = False

    def mark_spam(self, user):
        """
        Check if user has already marked Spam or not and mark accordingly.
        Returns True if spamming for the first time.
        Returns False if already marked spam
        """
        vote, created = Vote.objects.get_or_create(content=self, user=user)
        if vote.spam_moderated:
            # If spam flag was moderated. You can't operate again
            return

        if vote.spam:
            # If already marked spam. Clear the spam
            vote.spam = False
            self.spam_count -= 1
        else:
            vote.spam = True
            self.spam_count += 1
        vote.save()
        self.save()

    def reset_spam_flags(self):
        """
        Resets spam counter and mark all spam flag's moderation to True
        """
        spammers = Vote.objects.filter(content=self, spam=True)
        spammers.update(spam_moderated=True)
        self.spam_count = 0
        self.save()

    def vote_up(self, user):
        """
        Voting is like toggle button. Voting twice will clear your vote
        """
        vote, created = Vote.objects.get_or_create(content=self, user=user)
        if vote.downvote:
            # If downvoted
            vote.upvote = True
            vote.downvote = False
            self.upvotes += 1
            self.downvotes -= 1
        elif vote.upvote:
            vote.upvote = False
            self.upvotes -= 1
        else:
            vote.upvote = True
            self.upvotes += 1
        self.popularity = self.upvotes - self.downvotes
        vote.save()
        self.save()

    def vote_down(self, user):
        """
        Voting is like toggle button. Voting twice will clear your vote
        """
        vote, created = Vote.objects.get_or_create(content=self, user=user)
        if vote.upvote:
            # If downvoted
            vote.downvote = True
            vote.upvote = False
            self.downvotes += 1
            self.upvotes -= 1
        elif vote.downvote:
            vote.downvote = False
            self.downvotes -= 1
        else:
            vote.downvote = True
            self.downvotes += 1
        self.popularity = self.upvotes - self.downvotes
        vote.save()
        self.save()

    def pre_delete(self):
        """ Dummy function """
        print "Dummy content delete"

    def get_author(self):
        """ Returns none if anonymous is True else returns author object """
        if self.anonymous:
            return None
        else:
            return get_user_info(self.author)


class Thread(Content):
    """ Thread for a discussion Forum """

    title = models.CharField(max_length=SHORT_TEXT)

    # Tags
    tags = models.ManyToManyField(Tag, related_name="thread_tags")

    subscription = models.OneToOneField(
        Subscription,
        related_name="thread_subscribers"
    )

    def save(self, *args, **kwargs):
        """ overriding save method """
        if self.pk is None:
            subscription = Subscription()
            subscription.save()
            self.subscription = subscription
        super(Thread, self).save(*args, **kwargs)


class Comment(Content):
    """ Comment class for discussion forum """

    thread = models.ForeignKey(Thread, related_name="Comment_Thread")


class Reply(Content):
    """ Reply class for discussion forum """

    # Used for directly getting parent of parent for reply
    thread = models.ForeignKey(Thread, related_name="Thread_Reply")

    comment = models.ForeignKey(Comment, related_name="Reply_Comment")


class Vote(models.Model):
    """
    Table for storing vote and spam for specific content by specific user
    """

    user = models.ForeignKey(User, related_name="vote_user", db_index=True)
    content = models.ForeignKey(Content, related_name="vote_content",
                                db_index=True)
    upvote = models.BooleanField(default=False)
    downvote = models.BooleanField(default=False)

    # spam_moderated will be enabled once moderated approve the spammed \
    # content and User spam flag won't count toward spam count then onwards
    spam = models.BooleanField(default=False, db_index=True)
    spam_moderated = models.BooleanField(default=False)

    class Meta:
        """ Meta """
        unique_together = ("user", "content")


class Notification(TimeKeeper):
    """ Table for storing notifications. This class/interface may change """

    subscription = models.ForeignKey(Subscription)
    notif_type = models.CharField(
        max_length=32,
        help_text="Help in grouping of notifications later on"
    )

    # Notification related info, link, users, reply/comment/thread object \
    # as appropriate
    info = models.TextField()

    is_processed = models.BooleanField(default=False)


@receiver(pre_delete, sender=Thread)
def update_thread_counter(sender, **kwargs):
    """ Decrease thread count by 1 """
    instance = kwargs['instance']
    instance.forum.thread_count -= 1
    instance.forum.save()


@receiver(pre_delete, sender=Comment)
def update_comment_counter(sender, **kwargs):
    """ Decrease thread count by 1 """
    instance = kwargs['instance']
    instance.thread.children_count -= 1
    instance.thread.save()


@receiver(pre_delete, sender=Reply)
def update_reply_counter(sender, **kwargs):
    """ Decrease thread count by 1 """
    instance = kwargs['instance']
    instance.comment.children_count -= 1
    instance.comment.save()