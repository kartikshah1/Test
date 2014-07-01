"""
    Contains database schema for user registration
"""

from uuid import uuid4

from django.db import models
from django.contrib.auth.models import User

from notification.views import activation_email, forgot_password_email

# Constants
SHORT_TEXT = 63
LONG_TEXT = 255


class Registration(models.Model):
    """
        Model for Storing Activation Records of users.
        They gets deleted once User get activation
    """
    user = models.ForeignKey(User, related_name='User_Registration')
    activation_key = models.CharField(max_length=32)

    def register(self, request):
        """ Generate a new random key """
        self.activation_key = uuid4().hex
        activation_email(user=self.user, activation_key=self.activation_key, request=request)

    def activate(self):
        """ Activate user object and delete the table """
        self.user.is_active = True
        self.user.save()
        self.delete()


class EmailUpdate(models.Model):
    """
        Model for storing activation record for Email Validation
    """
    user = models.ForeignKey(User, related_name='User_EmailUpdate')
    new_email = models.CharField(max_length=SHORT_TEXT)
    activation_key = models.CharField(max_length=32)

    def generate_key(self):
        """ Generate a new random key """
        self.activation_key = uuid4().hex

    def update_email(self):
        """ Update email to new one and delete EmailUpdate instance """
        self.user.email = self.new_email
        self.delete()


class ForgotPassword(models.Model):
    """
        Model for storing the users and a unique key related to it
        who requested for change of ForgotPassword
    """
    user = models.ForeignKey(User, related_name='User_ForgotPassword')
    activation_key = models.CharField(max_length=32)

    def generate_key(self, request):
        """ Generate a new random key """
        self.activation_key = uuid4().hex
        forgot_password_email(user=self.user, activation_key=self.activation_key, request=request)

    def update_password(self, passwd):
        """Update the password for the user"""
        self.user.set_password(passwd)
        self.user.save()
        self.delete()

    def __unicode__(self):
        return self.user.username + "  " + self.activation_key
