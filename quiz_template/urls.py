"""
Quiz_Template URL resolver file
"""

from django.conf.urls import include, patterns, url
from quiz_template.views import QuizViewSet, QuestionModuleViewSet, \
    QuestionMasterViewSet, QuestionScqViewSet, QuestionMcqViewSet, QuestionFixViewSet, \
    QuestionDesViewSet, UserSubmissionsViewSet, view
from rest_framework import routers


# Configuring routers
router = routers.DefaultRouter()
router.register(r'quiz', QuizViewSet)
router.register(r'question_module', QuestionModuleViewSet)
router.register(r'question_master', QuestionMasterViewSet)
router.register(r'question_scq', QuestionScqViewSet)
router.register(r'question_mcq', QuestionMcqViewSet)
router.register(r'question_fix', QuestionFixViewSet)
router.register(r'question_des', QuestionDesViewSet)
router.register(r'submission', UserSubmissionsViewSet)


urlpatterns = patterns(
    '',
    url(r'^api/', include(router.urls)),
    url(r'^view/', view, name="view"),
)
