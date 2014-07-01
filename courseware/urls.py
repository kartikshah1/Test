"""
URL Mapping for Courseware API
This is API for accessing course information
"""

from django.conf.urls import include, patterns, url

from rest_framework.routers import DefaultRouter

from courseware.viewsets.category import ParentCategoryViewSet, CategoryViewSet
from courseware.viewsets.course import CourseViewSet, CourseInfoViewSet, OfferingViewSet
from courseware.viewsets.group import GroupViewSet
from courseware.viewsets.vconcept import ConceptViewSet
from courseware import views

# Configuring ROUTERs
router = DefaultRouter()

router.register(r'parent_category', ParentCategoryViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'course', CourseViewSet)
router.register(r'offering', OfferingViewSet)
router.register(r'courseinfo', CourseInfoViewSet)
router.register(r'group', GroupViewSet)
router.register(r'concept', ConceptViewSet)
router.register(r'all_courses', CourseViewSet)

urlpatterns = patterns(
    '',
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', views.parent_categories, name='parent_categories'),
    url(r'^(?P<pk>[1-9][0-9]*)$', views.categories, name='categories'),
    url(r'^category/(?P<pk>[1-9][0-9]*)$', views.courses, name='courses'),
    url(r'^course/(?P<pk>[1-9][0-9]*)/(?P<ref>-?[0-9]*)$', views.course, name='course'),
    url(r'^add_course', views.add_course, name='add_course'),
    url(r'^pastcourses/', views.to_do, name="pastcourses"),
    url(r'^courseslist/', views.mycourselist, name='mycourselist'),
    url(r'^myofferings/', views.instructor_courses, name="myofferings"),
    url(r'^mytextbooks/', views.content_developer_courses, name="mytextbooks"),
    url(r'^mycourses/', views.student_courses, name='mycourses'),
    url(r'^syllabus/(?P<pk>[1-9][0-9]*)$', views.syllabus, name='syllabus')
)
