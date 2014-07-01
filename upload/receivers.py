from django.db import models

# Pre_Delete receiver. Deletes all the files of the instance passed as input.
def delete_files(sender, instance, **kwargs):
    for field in instance._meta.fields: 
        if isinstance(field, models.FileField):
            filefield = getattr(instance, field.name)
            if filefield:
                filefield.delete(save=False)