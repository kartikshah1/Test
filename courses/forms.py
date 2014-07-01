'''
Created on May 16, 2013
@author: aryaveer
'''

from django.forms.util import ErrorList

from django import forms
from courses.models import Role

class DivErrorList(ErrorList):
    def __unicode__(self):
        return self.as_divs()
    def as_divs(self):
        if not self: return u''
        return u'<div class="alert alert-error">%s</div>' % ''.join([u'<div class="error">%s</div>' % e for e in self])

class RoleForm(forms.Form):
    roles = (
             ('S','Student'),
             ('T', 'Teacher')
            )
    role = forms.ChoiceField(choices=roles)

    def __init__(self, *args, **kwargs):
        kwargs['error_class']=DivErrorList
        super(RoleForm, self).__init__(*args, **kwargs)

class JoinCourseForm(forms.Form):
    choices = [('S', 'Student'),]
    name_or_id = forms.CharField(label="Course Name or course code")
    role = forms.ChoiceField(
                        choices=choices,
                        label="Join as",
                    )

    def __init__(self, *args, **kwargs):
        kwargs['error_class']=DivErrorList
        super(JoinCourseForm, self).__init__(*args, **kwargs)

    def clean_name_or_id(self):
        # form field has been cleaned and value is stored in self.cleaned_data
        data = self.cleaned_data['name_or_id']
        try:
            self.course = self.course_class.objects.get(name=data)
        except self.course_class.DoesNotExist:
            raise forms.ValidationError(["This course does not exist."])

        return data

    def clean(self):
        cleaned_data = super(JoinCourseForm, self).clean()
        if self.errors: return cleaned_data

        has_joined = Role.objects.filter(user=self.current_user, course=self.course, role=cleaned_data.get('role')).count()

        if bool(has_joined):
            self._errors['name_or_id'] = self.error_class(["You have already joined this course"])
        elif self.current_user == self.course.creater:
            self._errors['name_or_id'] = self.error_class(["You are instructor of this course. You cannot join"])

        return cleaned_data