from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from dajaxice.core import dajaxice_config
from dajaxice.core import dajaxice_autodiscover
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

dajaxice_autodiscover()
admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'grader.views.home', name='home'),
    # url(r'^grader/', include('grader.foo.urls')),
    (r'^cribs/', include('cribs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^accounts/', include('userena.urls')),
    url(r'^messages/', include('userena.contrib.umessages.urls')),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    url(r'^upload/', include('upload.urls')),
    url(r'^download/', include('download.urls')),
    url(r'^courses/', include('courses.urls')),
    url(r'^assignments/', include('assignments.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^evaluate/', include('evaluate.urls')),
    url(r'^$', 'courses.views.index', name='courses_index'), # TODO: temporary page change it later.
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
