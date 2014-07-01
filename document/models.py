from django.db import models
from uuid import uuid4
import json

# Create your models here.

SHORT_TEXT = 255
LARGE_TEXT = 1023
UUID_TEXT = 32


class Document(models.Model):
    """
    Class for storing General HTML Markup doument which can have \
    multiple sections.
    Will be used in additional course info pages
    """
    title = models.CharField(max_length=SHORT_TEXT)  # Page/Link Title
    uid = models.CharField(max_length=UUID_TEXT)  # Unique ID for Document
    is_heading = models.BooleanField(default=False)

    #This document can be link to another page too
    is_link = models.BooleanField(default=False)
    link = models.URLField(max_length=SHORT_TEXT, blank=True)

    description = models.TextField(
        blank=True,
        help_text="Short description/text for document \
            Leave it blank for no display"
    )
    playlist = models.TextField(default="[]")

    def save(self, *args, **kwargs):  # pylint: disable=W0613
        """ Overriding save method for assigning random uid on create """
        if not self.pk:
            self.uid = uuid4().hex
        super(Document, self).save(*args, **kwargs)

    def sections(self):
        """ Returns array of sections of this documents """
        sects = Section.objects.filter(document=self)
        return [x.to_dict() for x in list(sects)]

    def to_dict(self):
        """ Returns dict object of this document """
        obj = {
            "title": self.title,
            "description": self.description,
            "id": self.pk
        }
        obj["sections"] = self.sections()
        _playlist = json.loads(str(self.playlist))
        N = len(_playlist)
        ordered_data = [""]*N
        for i in range(N):
            ordered_data[i] = obj["sections"][_playlist[i][1]]
        obj["sections"] = ordered_data
        return obj


class Section(models.Model):
    """
    This class will be subpart of Document Class. This stores part \
    of information
    """
    document = models.ForeignKey(
        Document,
        related_name="Document_Section",
        db_index=True)
    title = models.CharField(max_length=SHORT_TEXT)
    description = models.TextField()
    file = models.FileField(upload_to='uploads/section', null=True, blank=True)

    def to_dict(self):
        """ Returns dictionary format of this object """
        data = {
            "id": self.pk,
            "title": self.title,
            "description": self.description
        }
        if self.file:
            data["file"] = self.file.url
        return data
