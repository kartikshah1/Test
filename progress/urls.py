"""
Progress URL resolver file
"""

from django.conf.urls import patterns, url
from progress import views

urlpatterns = patterns(
    '',
    url(r'^(?P<course>[1-9][0-9]*)$', views.view_progress)
)
