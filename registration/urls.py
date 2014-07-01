"""
    URL mappings for Registration
"""

from django.conf.urls import include, patterns, url
from registration import views
from registration.views import UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'register', UserViewSet)

urlpatterns = patterns(
    '',
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')),
    url(r'^signup/', views.signup, name="signup"),
    url(r'^login/', views.login_, name="login"),
    url(r'^logout/', views.logout_, name="logout"),
    url(r'^activate/(?P<key>\w{32})', views.activate, name="activate"),
    url(r'^forgotpassword/', views.forgot_password, name="forgotpassword"),
    url(r'^changepassword/(?P<key>\w{32})',
        views.update_password,
        name="changepassword"),
)
