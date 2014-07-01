"""
    Contains views for the Email Notification app
"""

from django.template.loader import get_template
from django.template import RequestContext

from notification.models import NotificationEmail


def activation_email(user, activation_key, request):
    """
        Function to send email to user stored email address for activation of account
    """
    html_activation_template = get_template("notification/html_activation_email.html")

    text_activation_template = get_template("notification/text_activation_email.html")

    parameters = {
        "username": user.username,
        "activation_key": activation_key
    }
    html_activation_body = html_activation_template.render(RequestContext(request, parameters))
    text_activation_body = text_activation_template.render(RequestContext(request, parameters))

    email = NotificationEmail(user=user, service="register_user",
                              email_subject="Verify Account for Elearning",
                              text_email_body=text_activation_body,
                              html_email_body=html_activation_body)
    email.send_email()


def forgot_password_email(user, activation_key, request):
    """
        Function to send email to user to update password which was lost
    """
    html_fp_template = get_template("notification/html_forgot_password_email.html")

    text_fp_template = get_template("notification/text_forgot_password_email.html")

    parameters = {
        "username": user.username,
        "activation_key": activation_key
    }
    html_fp_body = html_fp_template.render(RequestContext(request, parameters))
    text_fp_body = text_fp_template.render(RequestContext(request, parameters))

    email = NotificationEmail(user=user, service="update_password",
                              email_subject="Change Password for Elearning",
                              text_email_body=text_fp_body,
                              html_email_body=html_fp_body)
    email.send_email()
