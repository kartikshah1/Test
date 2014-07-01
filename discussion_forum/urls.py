"""
URL Mapping for Discussion Forum
This is API for accessing discussion Forum
"""

from django.conf.urls import include, patterns, url

from rest_framework import routers

from discussion_forum import views

# Configuring routers
router = routers.DefaultRouter()
router.register(r'forum', views.DiscussionForumViewSet)
router.register(r'tag', views.TagViewSet)
router.register(r'user_setting', views.UserSettingViewSet)
router.register(r'content', views.ContentViewSet)
router.register(r'thread', views.ThreadViewSet)
router.register(r'comment', views.CommentViewSet)
router.register(r'reply', views.ReplyViewSet)

urlpatterns = patterns(
    '',
    url(r'^$', views.forum, name='forum'),
    url(r'^admin/$', views.forum_admin, name='forum_admin'),
    url(r'^api/', include(router.urls)),
)
