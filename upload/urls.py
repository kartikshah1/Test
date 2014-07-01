from django.conf.urls.defaults import patterns, url


urlpatterns = patterns('upload.views',
    url(r'^$', 'upload', name='upload'),
    #url(r'^(?P<assignmentID>\d+)$', 'uploadAssignment', name='upload_uploadassignment'),
    url(r'^showall/(?P<assignmentID>\d+)$', 'showAllSubmissions', name='upload_showAllSubmissions'),
    url(r'^mysubmissions/(?P<courseID>\d+)$', 'my_submissions', name='upload_mysubmissions'),
)