"""
URL Mapping for Document API
"""

from django.conf.urls import include, patterns, url

from rest_framework.routers import DefaultRouter

from document.views import DocumentViewSet, SectionViewSet

# Configuring ROUTERs
router = DefaultRouter()

router.register(r'page', DocumentViewSet)
router.register(r'section', SectionViewSet)

urlpatterns = patterns(
    '',
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')),
)
