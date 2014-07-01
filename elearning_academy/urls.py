"""
    Root URL resolver file
"""

from django.conf.urls import patterns, include, url
from django.contrib import admin

from dajaxice.core import dajaxice_config
from dajaxice.core import dajaxice_autodiscover

from elearning_academy import settings
import views

admin.autodiscover()

urlpatterns = patterns(  # pylint: disable=C0103
    '',

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^$', views.index, name='index'),

    url(r'^old/', views.old_site, name='old_site'),
    url(r'^team/', views.team, name='team'),
    url(r'^mission/', views.mission, name='mission'),
    url(r'^contact/', views.contact, name='contact'),

    url(r'^accounts/', include('registration.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Django Static file serve
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT}),

    # Django Media file serve
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),

    url(r'^user/', include('user_profile.urls')),
    url(r'^notification/', include('notification.urls')),
    url(r'^forum/', include('discussion_forum.urls')),
    url(r'^quiz/', include('quiz.urls')),
    url(r'^courseware/', include('courseware.urls')),
    url(r'^concept/', include('concept.urls')),
    url(r'^video/', include('video.urls')),
    url(r'^document/', include('document.urls')),
    url(r'^progress/', include('progress.urls')),
    url(r'^quiz_template/', include('quiz_template.urls')),

    #grader
        (r'^cribs/', include('cribs.urls')),
    #url(r'^messages/', include('userena.contrib.umessages.urls')),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    url(r'^upload/', include('upload.urls')),
    url(r'^courses/', include('courses.urls')),
    url(r'^assignments/', include('assignments.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^evaluate/', include('evaluate.urls')),
    #url(r'course^$', 'courses.views.index', name='courses_index'), # TODO: temporary page change it later.
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
)
