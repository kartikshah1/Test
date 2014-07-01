"""
Concept URL resolver file
"""

from django.conf.urls import include, patterns, url
from concept import views
from courseware.viewsets.vconcept import ConceptViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'concept', ConceptViewSet)

urlpatterns = patterns(
    '',
    url(r'^api/', include(router.urls)),
    url(r'^(\d+)/$', views.view_concept, name="view"),
    #url(r'^(\d+)/edit/$', views.view_content_developer,
    #    name="edit_concept_content_developer"),
)
