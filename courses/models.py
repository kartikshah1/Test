from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from datetime import date

'''
termNames = ['spring', 'winter', 'fall', 'summer']
def termChoices():
    years = [date.today().year + i for i in range(-1,2)]
    return [(term +" "+ str(year), term +" "+ str(year)) for year in years for term in termNames]

class Course(models.Model):
    code = models.CharField(blank=False, max_length=20, help_text="Course code eg CS 101")
    name = models.CharField(blank=False, max_length=150, help_text="Course name")
    creater = models.ForeignKey(User)
    createdOn = models.DateTimeField(auto_now_add=True)
    lastModifiedOn = models.DateTimeField(auto_now=True)
    isActive = models.BooleanField(default=True)


    #TODO: make termChoices dynamic
    term = models.CharField(max_length=50,
                            blank=False,
                            choices=termChoices()
                            )

    courseDescription= models.TextField(default="None")

    class Meta:
        unique_together = ("code", "creater", "term")


class CourseForm(ModelForm):
    class Meta:
        model = Course
        include = ('code', 'name', 'isActive', 'term', 'courseDescription')
        exclude = ('creater')

        widgets = {}

        f = model._meta.get_field('code')
        formField = f.formfield() 
        widgets['code'] = type(formField.widget)(attrs={'title': f.help_text})


class Role(models.Model):
    user = models.ForeignKey(User)
    course = models.ForeignKey(Course)

    role = models.CharField(max_length=50)
'''
