from django.db import models
from django.contrib.auth.models import User

from assignments.models import Assignment

class Crib(models.Model):
    assignment = models.ForeignKey(Assignment)
    created_by = models.ForeignKey(User)
    title = models.CharField(max_length=512)
    crib_detail = models.TextField()
    is_resolved = models.BooleanField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified_on = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    crib = models.ForeignKey(Crib)
    posted_by = models.ForeignKey(User)
    comment = models.TextField()
    posted_on = models.DateTimeField(auto_now_add=True)