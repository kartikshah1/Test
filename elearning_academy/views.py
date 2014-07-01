from django.shortcuts import render, redirect

from elearning_academy import settings


def index(request):
    """
        this is the home page for elearning website
    """
    if request.user.is_authenticated():
        return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'elearning_academy/welcome.html')


def contact(request):
    return render(request, 'elearning_academy/contactus.html')


def team(request):
    return render(request, 'elearning_academy/team.html')


def mission(request):
    return render(request, 'elearning_academy/mission.html')

def old_site(request):
    return render(request, 'elearning_academy/old.html')
