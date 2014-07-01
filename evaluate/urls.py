'''
Created on May 22, 2013
@author: aryaveer
'''
from django.conf.urls import patterns, url

urlpatterns = patterns('evaluate.views',
    url(r'^(?P<submissionID>\d+)$', 'evaluateAssignment', name='evaluate_evaluateassignment'),
    url(r'^submission/(?P<submissionID>\d+)$', 'evaluateSubmission', name='evaluate_evaluatesubmission'),
    url(r'^output/(?P<programID>\d+)$', 'checkOutput', name='evaluate_checkoutput'),
    url(r'^result/(?P<submissionID>\d+)$', 'showResult', name='evaluate_showresult'),
    url(r'^evalall/(?P<assignmentID>\d+)$', 'eval_all_submissions', name='evaluate_evalallsubmissions'),
    url(r'^practice/(?P<submissionID>\d+)$', 'run_practice_test', name='evaluate_runpracticetest'),
    url(r'^details/(?P<submissionID>\d+)$', 'evaluation_details', name='evaluate_evaluationdetails'),
    url(r'^completedetails/(?P<assignmentID>\d+)$', 'complete_evaluation_details', name='evaluate_completeevaluationdetails'),
)