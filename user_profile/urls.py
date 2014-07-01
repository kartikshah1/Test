"""
    URL mappings for User Profile
"""

from django.conf.urls import patterns, url
from user_profile import views
from django.conf import settings

urlpatterns = patterns(
    '',
    url(r'^home/', views.home, name="home"),
    url(r'^view-profile/', views.view_profile, name="view-profile"),
    url(r'^all/(?P<key>college|major|company)', views.all_data, name="data"),
    url(r'^settings/', views.view_settings, name="settings"),
    url(r'^switch-mode/', views.switch_mode, name="switch-mode"),
)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns(
        '',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}))
