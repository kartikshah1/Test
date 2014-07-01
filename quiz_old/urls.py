"""
Quiz URL resolver file
"""

from django.conf.urls import include, patterns, url
from quiz.views import QuizViewSet, QuestionModuleViewSet, \
    FixedAnswerQuestionViewSet, SubmissionViewSet, QuestionViewSet, view, admin
from rest_framework import routers




# Configuring routers
router = routers.DefaultRouter()
router.register(r'quiz', QuizViewSet)
router.register(r'question_module', QuestionModuleViewSet)
router.register(r'question', QuestionViewSet)
router.register(r'fixed_answer_question', FixedAnswerQuestionViewSet)
router.register(r'submission', SubmissionViewSet)

urlpatterns = patterns('',
    url(r'^api/', include(router.urls)),
    url(r'^view/', view, name="view"),
    url(r'^admin/', admin, name="admin")
)
