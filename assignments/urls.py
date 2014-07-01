from django.conf.urls import patterns, url
from assignments.views import CreateTestcaseWizard, EditTestcaseWizard
from assignments.forms import TestcaseForm, TestcaseForm2

urlpatterns = patterns('assignments.views',
    url(r'^(?P<courseID>\d+)$', 'index', name='assignments_index'),
    url(r'^create/(?P<courseID>\d+)$', 'createAssignment', name='assignments_create'),
    url(r'^details/(?P<assignmentID>\d+)$', 'detailsAssignment', name='assignments_details'),
    url(r'^edit/(?P<assignmentID>\d+)$', 'editAssignment', name='assignments_edit'),
    url(r'^delete/(?P<assignmentID>\d+)$', 'removeAssignment', name='assignments_removeassignment'),
    url(r'^delete/submission/(?P<uploadID>\d+)$', 'deleteSubmission', name='assignments_deleteassignment'),
    url(r'^program/create/(?P<assignmentID>\d+)$', 'createProgram', name='assignments_createprogram'),
    url(r'^program/details/(?P<programID>\d+)$', 'detailProgram', name='assignments_detailsprogram'),
    url(r'^program/edit/(?P<programID>\d+)$', 'editProgram', name='assignments_editprogram'),
    url(r'^program/delete/(?P<programID>\d+)$', 'removeProgram', name='assignments_removeprogram'),
    url(r'^program/list/$', 'programList', name='assignment_programlist'),
    url(r'^testcase/create/(?P<programID>\d+)$', CreateTestcaseWizard.as_view([TestcaseForm, TestcaseForm2]), name='assignments_createtestcase'),
    url(r'^testcase/edit/(?P<testcaseID>\d+)$', EditTestcaseWizard.as_view([TestcaseForm, TestcaseForm2]), name='assignments_edittestcase'),
    url(r'^testcase/details/(?P<testcaseID>\d+)$', 'detailTestcase', name='assignments_detailstestcase'),
    url(r'^testcase/delete/(?P<testcaseID>\d+)$', 'removeTestcase', name='assignments_removetestcase'),
    url(r'^testcase/list/$', 'testcaseList', name='assignment_testcaselist'),
    url(r'^config/(?P<assignmentID>\d+)$', 'config_safeexec_params', name='assignments_configsafeexecparams'),
)