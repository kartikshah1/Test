"""
    Contains database schema for Email Notifications
"""

from django.db import models
from django.contrib.auth.models import User
from elearning_academy import settings

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(subject, text_msg, from_email, to_email_list, html_msg):
    """
        Send email to list of reciepients using smtp
        Django mail is not used because it uses only 3 authentication method
        and is a smtp server propogates MD5 but does not support then it fails
        work around is from http://www.harelmalka.com/?p=94
        :arg subject: Email subject, preferably be not None otherwise mail
                        can be rendered as spam
        :arg text_msg: (string) Message to be sent in plain text format
        :arg from_email: email id to be displayed in From field of header
        :arg to_email_list: a list of email ids to which to send the email
        :arg html_msg: (String) Message to be sent in text/html format
    """

    server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    server.starttls()
    server.ehlo()
    server.esmtp_features['auth'] = 'LOGIN PLAIN'
    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

    mail = MIMEMultipart("alternative")
    mail['Subject'] = subject
    mail['From'] = from_email
    mail.attach(MIMEText(text_msg, 'plain'))
    mail.attach(MIMEText(html_msg, 'html'))

    for to_email in to_email_list:
        mail['To'] = to_email
        server.sendmail(from_email, to_email, mail.as_string())


class NotificationEmail(models.Model):
    """
        Model to store email content to be consumed by cron
        worker and sent to Users
    """

    user = models.ForeignKey(User, related_name='Email_Notification')
    service = models.CharField(max_length=50)
    email_subject = models.CharField(max_length=50)
    text_email_body = models.TextField()
    html_email_body = models.TextField()

    def send_email(self):
        '''
            Sends Notification Mail using <service>@elearning.com
            using SMTP using global settings
        '''
        from_email = "no_reply_%s@elearning.com" % (self.service)
        send_mail(subject=self.email_subject, text_msg=self.text_email_body,
                  from_email=from_email, to_email_list=[self.user.email],
                  html_msg=self.html_email_body)
