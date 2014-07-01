"""
    Make the variables in settings.py as globally available in templates
"""

from django.conf import settings
from user_profile.models import CustomUser


def my_global_name(request):
    """
        Function is context processor for templates which makes the
        user defined variables as globally available.
    """
    if (request.user.is_authenticated()):
        customuser = CustomUser.objects.filter(user=request.user)
    else:
        customuser = []
    if len(customuser) == 0:
        is_instructor = False
        is_content_developer = False
    else:
        is_instructor = customuser[0].is_instructor
        is_content_developer = customuser[0].is_content_developer
    return {

        "MY_SERVER": settings.MY_SERVER,
        "COPYRIGHT_YEAR": settings.COPYRIGHT_YEAR,
        "MY_SITE_NAME": settings.MY_SITE_NAME,
        "IS_INSTRUCTOR": is_instructor,
        "IS_CONTENT_DEVELOPER": is_content_developer,
        "favicon": settings.TITLE_ICON
    }
