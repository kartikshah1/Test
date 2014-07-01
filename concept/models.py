""" Models related to concept """

from django.db import models

# Create your models here.

from quiz.models import Quiz
from django.contrib.auth.models import User
from courseware.models import Document


class ConceptQuizHistory(models.Model):
    """
    Class for ConceptQuizHistory
    """
    quiz = models.ForeignKey(Quiz)
    user = models.ForeignKey(User, db_index=True)
    seen_status = models.BooleanField(default=False)
    times_seen = models.IntegerField(default=0)


class ConceptDocumentHistory(models.Model):
    """
    Class for ConceptDocumentHistory
    """
    document = models.ForeignKey(Document)
    user = models.ForeignKey(User, db_index=True)
    seen_status = models.BooleanField(default=False)
    times_seen = models.IntegerField(default=0)
