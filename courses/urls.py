from django.conf.urls import patterns, url

urlpatterns = patterns('courses.views',
    url(r'^$', 'index', name='courses_index'),
    #url(r'^(?P<courseid>\d+)$', 'courseInfo', name='courses_courseInfo'),
    #url(r'^join/(?P<courseid>\d+)$', 'joinCourse', name='courses_joincourse'), TODO: 
    #url(r'^join/(?P<courseid>\d+)$', 'joinCourse', name='courses_joincourse'),
    #url(r'^leave/(?P<courseid>\d+)$', 'leaveCourse', name='courses_leavecourse'),
    #url(r'^searchcourses/$', 'searchCourse', name='courses_searchcourse'),
    #url(r'^edit/(?P<courseid>\d+)$', 'editCourse', name='courses_editCourse'),
    #url(r'^all/$', 'all_courses', name='courses_allcourses'),
    #url(r'^create/$', 'create_course', name='courses_createcourse'),
    #url(r'^delete/(?P<courseid>\d+)$', 'delete_course', name='courses_deletecourse'),
)
