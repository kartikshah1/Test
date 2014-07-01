"""
    This file contains abstracted functionality for more convenience
"""

from django.db import models
from django.contrib.auth.models import User

SHORT_TEXT = 255
LARGE_TEXT = 1023


class Votable(models.Model):
    """
    This is Non-Abstract class which can be inherited by any class for \
    getting voting functionality.
    Meant to be use for elements which requires voting.

    We have included this class into discussion_forum.models.Content for\
    efficiency reasons.
    """
    # Indexed for efficient sorting on colum
    upvotes = models.IntegerField(default=0, db_index=True)
    downvotes = models.IntegerField(default=0, db_index=True)

    # popularity = upvotes - downvotes
    popularity = models.IntegerField(default=0, db_index=True)

    upvoters = models.ManyToManyField(User, related_name='_upvoters')
    downvoters = models.ManyToManyField(User, related_name='_downvoters')

    def vote_up(self, user):
        """
        perform checks and vote up accordingly
        """
        if self.upvoters.filter(upvoters_pk=user.pk).exists():
            return
        elif self.downvoters.filter(downvoters_pk=user.pk).exists():
            self.downvotes -= 1
            self.upvotes += 1
            self.downvoters.remove(user)
            self.upvoters.add(user)
        else:
            self.upvotes += 1
            self.upvoters.add(user)
        self.save()

    def vote_down(self, user):
        """
        perform checks and vote up accordingly
        """
        if self.downvoters.filter(downvoters__pk=user.pk).exists():
            return
        elif self.upvoters.filter(upvoters__pk=user.pk).exists():
            self.upvotes -= 1
            self.downvotes += 1
            self.upvoters.remove(user)
            self.downvoters.add(user)
        else:
            self.downvotes += 1
            self.downvoters.add(user)
        self.save()

    class Meta:  # pylint: disable=W0232
        """This class will have its own database table"""
        abstract = False


class TimeKeeper(models.Model):
    """
    Abstraction for storing creation and last edit time of database object
    """
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    modified = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:  # pylint: disable=W0232
        """This class won't have its own database table"""
        abstract = True


class HitCounter(models.Model):
    """
    Abstraction for counting hits of a particular object
    """
    hit_count = models.IntegerField(default=0)

    def make_hit(self):
        """ Increase hit_count and saves immediately """
        self.hit_count += 1
        self.save()

    class Meta:  # pylint: disable=W0232
        """This class won't have its own database table"""
        abstract = True


class Subscription(models.Model):
    """
    Abstracted idea of maintaining subscription list.
    Any object can have OneToOne relationship with this model
    """

    users = models.ManyToManyField(User, related_name='subscribers')

    def subscribe(self, user):
        """ Add user into subscriber list """
        self.users.add(user)

    def unsubscribe(self, user):
        """ Remove user from subscriber list """
        self.users.remove(user)

    def subscribers(self):
        """ Returns all the users """
        return self.users.all()

    def is_subscribed(self, user):
        """ Return True if user is subcribed else returns False """
        return Subscription.objects.filter(pk=self.pk,
                                           users__pk=user.pk).exists()
