"""
This file contains the course related models
"""

from django.db import models
from django.contrib.auth.models import User


from video.models import Video
from quiz.models import Quiz, QuizHistory
from discussion_forum.models import DiscussionForum
from document.models import Document

import json

from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

SHORT_TEXT = 255
LARGE_TEXT = 1023
UUID_TEXT = 32

COURSE_CHOICES = (
    ('T', 'Textbook'),
    ('O', 'Offering'),
    )

GRADE_CHOICES = (
    ('FR', 'Fail'),
    ('AA', '10'),
    ('AB', '9'),
    ('BB', '8'),
    ('BC', '7'),
    ('CC', '6'),
    ('CD', '5'),
    ('DD', '4'),
    ('PP', 'Pass'),
    ('DN', 'Did not Complete'),
    )

ENROLLMENT_TYPE_CHOICES = (
    ('O', 'Open'),
    ('M', 'Moderated'),
    )

ENROL_CHOICES = (
    ('A', 'Active'),
    ('P', 'Pending Approval'),
    ('U', 'Unenrolled')
    )


class ParentCategory(models.Model):
    """Model for storing the parent categories"""
    title = models.CharField(max_length=SHORT_TEXT, blank=False, unique=True)

    def __unicode__(self):
        return self.title


class Category(models.Model):
    """
    This class contains all the category of courses
    """
    parent = models.ForeignKey(
        ParentCategory,
        related_name="Parent",
        db_index=True
        )
    title = models.CharField(max_length=SHORT_TEXT)
    image = models.ImageField(upload_to='uploads/category_image', null=True, blank=True)
    content_developers = models.ManyToManyField(
        User,
        related_name="Category_User"
        )

    def __unicode__(self):
        return self.title


class CourseInfo(models.Model):
    """
    This class stores the general information about the course
    """
    start_time = models.DateField(db_index=True, null=True, blank=True)
    end_time = models.DateField(null=True, blank=True)

    # This field is used by the instructor/content dev. to publish any course.
    # Only if it is true can a course/offering be visible to others
    # When the field is false, instructor has the option to delete the course.
    # Once this field is made true the instructor can no longer change it. He will have to mail
    # the admin
    is_published = models.BooleanField(default=False)
    description = models.CharField(max_length=LARGE_TEXT, blank=True)

    end_enrollment_date = models.DateField(null=True, blank=True)

    # Default granularity to use for all questions of this course
    # default_granularity = models.TextField(null=True)

    # Default granularity to use for all questions of this course after hint
    # default_granularity_hint = models.TextField(null=True)


class Course(models.Model):
    """
    This class contains information about a course
    """

    # Indexed for efficient querying of courses
    category = models.ForeignKey(
        Category,
        related_name="Category_Course",
        db_index=True
        )

    #Course details for the front page
    title = models.CharField(max_length=SHORT_TEXT)
    image = models.ImageField(upload_to='uploads/course_image', blank=True)

    type = models.CharField(max_length=1, choices=COURSE_CHOICES, default='T')
    playlist = models.TextField(default="[]")
    forum = models.ForeignKey(DiscussionForum, related_name='Course_Forum')

    #Documents attached to course
    pages = models.ManyToManyField(Document, related_name='Course_Document')
    page_playlist = models.TextField(default="[]")

    max_score = models.IntegerField(default=0)

    course_info = models.OneToOneField(
        CourseInfo,
        related_name="CourseInfo_Course",
        null=True,
        blank=True
    )

    # Field to see if open registrations are allowed or moderator has to \
    # approve. Who approves and where it will be stored and then to send a \
    # notification is still left to do.
    enrollment_type = models.CharField(
        max_length=1,
        choices=ENROLLMENT_TYPE_CHOICES,
        default='M'
        )

    def save(self, *args, **kwargs):
        """ overriding save method """
        if self.pk is None:
            forum = DiscussionForum()
            forum.save()
            course_info = CourseInfo()
            course_info.save()
            self.forum = forum
            self.course_info = course_info
        super(Course, self).save(*args, **kwargs)

    def update_score(self, difference):
        self.max_score += difference
        self.save()


class Offering(Course):
    """
        This class extends the Course class. This has offering specific related fields
    """
    shortlisted_courses = models.ManyToManyField(Course, related_name='shortlistedCourses')

    def save(self, *args, **kwargs):
        self.type = 'O'
        super(Offering, self).save(*args, **kwargs)


class CourseHistory(models.Model):
    """
    This class contains history of the user in a course
    """
    course = models.ForeignKey(
        Course,
        related_name="CourseHistory_Course",
        db_index=True
        )

    user = models.ForeignKey(User, related_name="CourseHistory_User")

    # Details of the user
    grade = models.CharField(
        max_length=2,
        choices=GRADE_CHOICES,
        null=True
    )
    score = models.FloatField(default=0.0, null=True)

    # To see whether user is enrolled or not or the approval is pending, do not delete objects
    active = models.CharField(max_length=1, choices=ENROL_CHOICES, default='U')

    is_moderator = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)

    show_marks = models.BooleanField(default=True)

    class Meta:
        """
        Course and user combined should be unique
        """
        unique_together = ("course", "user")
        index_together = [
            ['user', 'course'],
        ]

    def progress(self):
        data = {}
        data['score'] = self.score
        data['max_score'] = self.course.max_score
        groups = Group.objects.filter(course=self.course)
        _playlist = json.loads(self.course.playlist)
        data['groups'] = []
        for groupid in _playlist:
            gh, created = GroupHistory.objects.get_or_create(
                group=groups[groupid[1]], user=self.user)
            data['groups'].append(gh.progress())
        return data

    def update_score(self, difference):
        self.score += difference
        self.save()


class Group(models.Model):
    course = models.ForeignKey(
        Course,
        related_name="Group_Course",
        db_index=True
    )
    # Details of the concept
    title = models.CharField(max_length=SHORT_TEXT, blank=False)
    image = models.ImageField(
        upload_to='uploads/group_image', blank=True)
    pages = models.ManyToManyField(Document)
    max_score = models.IntegerField(default=0)
    playlist = models.TextField(default="[]")
    description = models.CharField(max_length=LARGE_TEXT, blank=True)

    def update_score(self, difference):
        self.max_score += difference
        self.save()
        self.course.update_score(difference)


class GroupHistory(models.Model):
    """
    This class contains history of the user in a course
    """
    group = models.ForeignKey(
        Group,
        related_name="GroupHistory_Group",
        db_index=True
        )

    user = models.ForeignKey(User, related_name="GroupHistory_User")
    score = models.FloatField(default=0.0, null=True)
    #course_history = models.ForeignKey(
    #    CourseHistory,
    #   related_name="CourseHistory_GroupHistory",
    #   db_index=True
    #)

    class Meta:
        """
        Course and user combined should be unique
        """
        unique_together = ("group", "user")
        index_together = [
            ['user', 'group'],
        ]

    def progress(self):
        data = {}
        data['id'] = self.id
        data['title'] = self.group.title
        data['score'] = self.score
        data['max_score'] = self.group.max_score
        concepts = Concept.objects.filter(group=self.group)
        _playlist = json.loads(self.group.playlist)
        data['concepts'] = []
        for conceptid in _playlist:
            ch, created = ConceptHistory.objects.get_or_create(
                concept=concepts[conceptid[1]], user=self.user)
            data['concepts'].append(ch.progress())
        return data

    def update_score(self, difference):
        self.score += difference
        self.save()
        ch, created = CourseHistory.objects.get_or_create(course=self.group.course, user=self.user)
        ch.update_score(difference)


class Concept(models.Model):
    """
    This class contains the details about a concept
    """
    group = models.ForeignKey(
        Group,
        related_name="Concept_Group",
        db_index=True
    )

    # Details of the concept
    title_document = models.ForeignKey(Document, related_name='Concept_Title')
    title = models.CharField(max_length=SHORT_TEXT)
    image = models.ImageField(
        upload_to='uploads/concept_image', blank=True, null=True)
    max_score = models.IntegerField(default=0)
    playlist = models.TextField(default="[]")
    description = models.CharField(max_length=LARGE_TEXT, blank=True, null=True)

    #Many to many relations for the learning elements in the playlist
    videos = models.ManyToManyField(Video, related_name='Concept_Video')
    quizzes = models.ManyToManyField(Quiz, related_name='Concept_Quiz')
    pages = models.ManyToManyField(Document, related_name='Concept_Document')
    is_published = models.BooleanField(default=False)

    def update_score(self, difference):
        self.max_score += difference
        self.save()
        self.group.update_score(difference)


class ConceptHistory(models.Model):
    """
    This class contains history of the user in a concept
    """
    concept = models.ForeignKey(
        Concept,
        related_name="ConceptHistory_Concept",
        )
    user = models.ForeignKey(
        User,
        related_name="User_Concept"
        )
    #group_history = models.ForeignKey(
    #    GroupHistory,
    #    related_name="GroupHistory_ConceptHistory",
    #    db_index=True
    #    )
    score = models.FloatField(default=0.0)

    class Meta:
        """
        Concept and user combined should be unique
        """
        unique_together = ("concept", "user")
        index_together = [
            ['user', 'concept'],
        ]

    def progress(self):
        data = {}
        data['id'] = self.concept.id
        data['title'] = self.concept.title
        data['score'] = self.score
        data['max_score'] = self.concept.max_score
        quizzes = self.concept.quizzes.all()
        #_playlist = json.loads(self.group.playlist)
        data['quizzes'] = []
        for quizid in quizzes:
            qh, created = QuizHistory.objects.get_or_create(
                quiz=quizid, user=self.user)
            data['quizzes'].append(qh.progress())
        return data

    def update_score(self, difference):
        self.score += difference
        self.save()
        gh, created = GroupHistory.objects.get_or_create(group=self.concept.group, user=self.user)
        gh.update_score(difference)


class LearningElement(models.Model):
    """
    The abstract class for a learning element. Will be inherited by quiz and \
    video classes.
    """
    course = models.ForeignKey(
        Course,
        related_name="LearningElement_Course",
        db_index=True
    )
    concept = models.ForeignKey(
        Concept,
        related_name="LearningElement_Concept",
        db_index=True
        )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_public = models.BooleanField()

    #publish_time = models.DateTimeField()
    is_hidden = models.BooleanField(default=False)

    class Meta:
        """
        Making abstract = True
        """
        abstract = True


@receiver(pre_delete, sender=Concept)
def delete_quizzes_on_delete(sender, **kwargs):
    """ Delete all quizzes related to Concept and decrease max_score"""
    instance = kwargs['instance']
    # instance.group.update_score((-1*(instance.max_score)))
    #  WARNING : This might not work
    instance.quizzes.all().delete()
