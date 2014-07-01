"""
    Contains database schema for user profile
"""

from django.db import models
from django.contrib.auth.models import User
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from model_utils import Choices
from uuid import uuid4
from user_profile.countries import COUNTRIES
import json

# Constants
SHORT_TEXT = 63
LONG_TEXT = 255

GENDER_CHOICES = Choices(
    ('M', 'Male'),
    ('F', 'Female')
)

PRIVACY_CHOICES = (
    ('PB', 'Public'),
    ('PR', 'Private'),
    ('SU', 'Site Users')
)

DEGREE = Choices(
    ('BE', 'B.E.'),
    ('ME', 'M.E'),
    ('BTECH', 'B.Tech'),
    ('MTECH', 'M.Tech'),
    ('BTECH_MTECH', 'Dual Degree (B.Tech+M.Tech)'),
    ('BE_ME', 'Dual Degree (B.E.+M.E.)'),
    ('PHD', 'PhD'),
    ('MS', 'M.S.'),
    ('MS_PHD', 'Dual Degree (M.S.+PhD)'),
    ('MTECH_PHD', 'Dual Degree (M.Tech+PhD)')
)


class Major(models.Model):
    """
        Class to store degree major of student
    """
    major = models.CharField(max_length=SHORT_TEXT, null=False)


class College(models.Model):
    """
        Class to store list of colleges
    """
    college = models.CharField(max_length=LONG_TEXT, null=False)


#User Education model
class Education(models.Model):
    """
        Class for User Education details
    """
    user = models.ForeignKey(User)
    degree = models.CharField(max_length=SHORT_TEXT, null=False, default=DEGREE.BTECH,
                              choices=DEGREE)
    college = models.ForeignKey(College)
    major = models.ForeignKey(Major)
    start_date = models.DateField(blank=False, null=True)
    end_date = models.DateField(blank=True, null=True)

    def start_date_to_string(self):
        """
            Return the start date for education in DD Month YYYY
        """
        if self.start_date:
            return self.start_date.strftime("%d %B %Y")
        else:
            return ""

    def end_date_to_string(self):
        """
            Return the end date for education in DD Month YYYY
        """
        if self.end_date:
            return self.end_date.strftime("%d %B %Y")
        else:
            return ""

    def get_json(self):
        """
            Return the education record in form of a json
        """
        return {
            'id': self.id,
            'degree': self.get_degree_display(),
            'college': self.college.college,
            'major': self.major.major,
            'start_date': self.start_date_to_string(),
            'end_date': self.end_date_to_string()
        }


#Company Names
class Company(models.Model):
    """
        Various companies which a user can have worked previously
    """
    company = models.CharField(max_length=SHORT_TEXT, blank=False)
    company_description = models.CharField(max_length=SHORT_TEXT, blank=False)

#User Work Experience Model
class Work(models.Model):
    """
        Class for User Work Experience details
    """
    user = models.ForeignKey(User)
    company = models.ForeignKey(Company)
    position = models.CharField(max_length=SHORT_TEXT, blank=False)
    description = models.CharField(max_length=LONG_TEXT)
    start_date = models.DateField(blank=False, null=True)
    end_date = models.DateField(blank=True, null=True)

    def start_date_to_string(self):
        """
            Return the start date for work in DD Month YYYY
        """
        if self.start_date:
            return self.start_date.strftime("%d %B %Y")
        else:
            return ""

    def end_date_to_string(self):
        """
            Return the end date for work in DD Month YYYY
        """
        if self.end_date:
            return self.end_date.strftime("%d %B %Y")
        else:
            return ""

    def get_json(self):
        """
            Return the Work record in form of a json
        """
        return {
            'id': self.id,
            'company': self.company.company,
            'position': self.position,
            'description': self.description,
            'start_date': self.start_date_to_string(),
            'end_date': self.end_date_to_string()
        }


# User profile model
class UserProfile(models.Model):
    """
    Class of user profile details
    """
    user = models.OneToOneField(User, primary_key=True,
                                related_name='User_UserProfile')
    uid = models.CharField(max_length=32)

    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    photo = models.ImageField(upload_to='static/img/', blank=True, null=True)
    mobile = models.CharField(max_length=10, null=True)
    place_city = models.CharField(max_length=SHORT_TEXT, blank=True, null=True)
    place_state = models.CharField(max_length=SHORT_TEXT, blank=True, null=True)
    place_country = models.CharField(max_length=SHORT_TEXT,
                                     choices=COUNTRIES, blank=True, null=True)

    privacy = models.CharField(max_length=2, choices=PRIVACY_CHOICES, blank=True, null=True)

    about = models.CharField(max_length=LONG_TEXT, blank=True, null=True)
    interests = models.CharField(max_length=LONG_TEXT, blank=True, null=True)

    website_twitter = models.URLField(max_length=LONG_TEXT, blank=True, null=True)
    website_facebook = models.URLField(max_length=LONG_TEXT, blank=True, null=True)

    def generate_user_id(self):
        """ Generate a random user id """
        self.uid = uuid4().hex

    def get_user_id(self):
        """ Return the user's user id """
        return self.uid

    def get_user_address(self):
        """
        Return the address of the user by concatenating city, state and country
        """
        return self.place_city + ", " + self.place_state + ", "\
            + self.place_country

    def dob_to_string(self):
        """ Convert the DateField to a printable string """
        if self.dob:
            return self.dob.strftime("%d %B %Y")
        else:
            return ""

    def education_list(self):
        """
            Return a List of json of education record of the user
            TODO(vgagrani): sort the list in terms of start time - Latest first
        """
        education_records = Education.objects.filter(user=self.user)
        education_list = []
        for record in education_records:
            education_list.append(record.get_json())
        return education_list

    def work_list(self):
        """
            Return a list of json of work record of the user
            TODO(vgagrani): sort the list in terms of start time - Latest first
        """
        work_records = Work.objects.filter(user=self.user)
        work_list = []
        for record in work_records:
            work_list.append(record.get_json())
        return work_list

    def toJson(self):
        """ Convert a UserProfile object to a json object """
        context = {}
        context["dob"] = self.dob_to_string()
        context["gender"] = self.get_gender_display()
        context["city"] = self.place_city
        context["state"] = self.place_state
        context["country"] = self.get_place_country_display()
        context["about"] = self.about
        context["interests"] = self.interests
        context["education_list"] = self.education_list()
        context["work_list"] = self.work_list()
        context["photo"] = "/media/" + str(self.photo)
        context["website_twitter"] = self.website_twitter
        context["website_facebook"] = self.website_facebook
        return json.dumps(context)


class CustomUser(models.Model):
    """
        Wrapper over django user to store the user mode of operation
    """
    STUDENT_MODE = 'S'
    INSTRUCTOR_MODE = 'I'
    CONTENT_DEVELOPER_MODE = 'C'
    MODE = (
        (STUDENT_MODE, 'Student Mode'),
        (INSTRUCTOR_MODE, 'Instructor Mode'),
        (CONTENT_DEVELOPER_MODE, 'Content Developer Mode')
    )
    user = models.OneToOneField(User)
    is_instructor = models.BooleanField(default=False)
    is_content_developer = models.BooleanField(default=False)
    default_mode = models.CharField(max_length=1, choices=MODE,
                                    help_text="Mode of Operation",
                                    default=STUDENT_MODE)


@receiver(post_save, sender=User)
def create_custom_user(sender, **kwargs):
    instance = kwargs['instance']
    if kwargs['created']:  # create
        customuser, created = CustomUser.objects.get_or_create(
            user=instance,
            )
