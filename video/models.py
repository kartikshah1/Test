"""
Models for Video
"""

from django.db import models
from django.contrib.auth.models import User
from model_utils.managers import InheritanceManager
from quiz.models import Quiz
from elearning_academy.settings import PROJECT_DIR

import subprocess, os

SHORT_TEXT = 63
LONG_TEXT = 255


class Video(models.Model):
    """
        Class for Video. Video though does not have a concept in it but it not
        independent from concept.
    """
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    video_file = models.FileField(upload_to='static/video/')
    other_file = models.FileField(upload_to='uploads/video_other/',
                                  null=True, blank=True)
    duration = models.IntegerField(default=0)

    def __unicode__(self):
        return self.title

    def get_video_file(self):
        """ Return the URL for Video File """
        return "/media/" + str(self.video_file)

    def get_other_file(self):
        """ Return URL for Slides """
        return "/media/" + str(self.other_file)

    def get_length(self):
        """
            Extract Duration of the video
        """
        root = os.path.join(PROJECT_DIR, os.path.normpath('elearning_academy/'))
        filename = os.path.join(root, os.path.normpath(self.get_video_file()[1:]))
        result = subprocess.Popen(['ffprobe', filename, "-v", "quiet", "-print_format", "json", "-show_format"],
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        line = [x for x in result.stdout.readlines() if "duration" in x]
        return int(float(line[0].strip(" \r\n,").split(":")[1].strip(" \"")))


class VideoHistory(models.Model):
    """
        Class for Video History
    """
    UPVOTE = 'U'
    DOWNVOTE = 'D'
    NOVOTE = 'N'
    VOTE_CHOICES = ((UPVOTE, "upvote"), (DOWNVOTE, 'downvote'), (NOVOTE, 'not voted'))

    video = models.ForeignKey(Video)
    user = models.ForeignKey(User, db_index=True)
    seen_status = models.BooleanField(default=False)
    times_seen = models.IntegerField(default=0)
    vote = models.CharField(max_length=1, choices=VOTE_CHOICES, help_text="Vote Type", default=NOVOTE)


class Marker(models.Model):
    """
        Class for a marker in Video. Each marker can be associated with atmost
        one Video.
    """
    SECTION_MARKER = 'S'
    QUIZ_MARKER = 'Q'
    MARKER_TYPES = (
        (SECTION_MARKER, 'Section Marker'),
        (QUIZ_MARKER, 'Quiz Marker')
    )
    video = models.ForeignKey(Video, related_name='markers')
    time = models.IntegerField(default=0, null=False)
    type = models.CharField(max_length=1, choices=MARKER_TYPES, help_text="Type of Marker")

    objects = InheritanceManager()

    class Meta:
        #abstract = True
        unique_together = ('video', 'time', 'type')
        ordering = ['time']

    def __unicode__(self):
        return 'Marker Id: %s, Video Id: %s, time: %d' % (self.id, self.video.id, self.time)


class SectionMarker(Marker):
    """
        Class for Section Marker
    """
    title = models.CharField(max_length=SHORT_TEXT, null=False)

    # set the type of marker in parent class
    def save(self, *args, **kwargs):
        self.type = self.SECTION_MARKER
        super(SectionMarker, self).save(*args, **kwargs)


class QuizMarker(Marker):
    """
        Class for Quiz type marker. It refers to a Quiz type object.
    """
    quiz = models.ForeignKey(Quiz)

    # set the type of marker in parent class
    def save(self, *args, **kwargs):
        self.type = self.QUIZ_MARKER
        super(QuizMarker, self).save(*args, **kwargs)
