"""
    Views for Progress
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from elearning_academy.permissions import get_mode

from rest_framework import status
from rest_framework.response import Response


@login_required
def view_progress(request, course):
    """
        View progress page of current user
    """
    mode = get_mode(request)
    if mode is not False:
        if mode == 'S':
            return render(request, 'progress/student_progress.html', {'courseId': course})
        elif mode == 'I':
            return render(request, 'progress/course_progress.html', {'courseId': course})
    return Response("Bad request", status.HTTP_400_BAD_REQUEST)
