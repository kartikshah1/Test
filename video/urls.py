"""
    URL Mapping for Video API
    This is API for view/edit/upload video
"""

from django.conf.urls import include, patterns, url

from rest_framework.routers import DefaultRouter

from video import views

# Configuring ROUTERs
router = DefaultRouter()

router.register(r'video', views.VideoViewSet)
router.register(r'marker', views.MarkerViewSet)

urlpatterns = patterns(
    '',
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')),
    url(r'^play_video', views.play_video, name="play_video"),
    url(r'^upload_video', views.upload_video, name="upload_video"),
    url(r'^edit_video', views.edit_video, name="edit_video"),
)
