from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete

from assignments.models import Assignment
from upload import receivers
import os

# Function to retrieve the upload path for an upload instance given the filename.
# Takes as input the instance of upload and the filename of the file uploading to the server.
# If the instance has assignment then the path is "user/assignment-id/filename", else it is "user/filename".
def get_upload_path(instance, filename):
    if instance.assignment:
        return os.path.join(
                    instance.owner.username,
                    str(instance.assignment.id),
                    filename
                )
    else:
        return os.path.join(
                    instance.owner.username,
                    filename
                )

# Model to represent submissions by students.
# It stores the owner of the submission, the assignment to which the subsmission belongs, filepath to the solution uploaded, date of uploading, 
# and a flag that denotes if the submission is stale w.r.t the assignment description.
class Upload(models.Model):
    owner = models.ForeignKey(User)
    assignment = models.ForeignKey(Assignment, blank=True, null=True)
    filePath = models.FileField(upload_to=get_upload_path)
    uploaded_on = models.DateTimeField(auto_now_add=True)
    is_stale = models.BooleanField(default=False) # stale means it requires re-submission.
pre_delete.connect(receivers.delete_files, sender=Upload, dispatch_uid="delete_submission")