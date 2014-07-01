from django.db import models
from django.db.models import signals
import os

from assignments.models import Testcase
from upload.models import Upload
from assignments.models import Program


def delete_files(sender, instance, **kwargs):
    for field in instance._meta.fields: 
        if isinstance(field, models.FileField):
            filefield = getattr(instance, field.name)
            if filefield:
                filefield.delete(save=False)

# Model to store the results of an assignment submission for all sections of the assignment.
# Stores only the submission and submitted files fields.
class AssignmentResults(models.Model):
    submission = models.ForeignKey(Upload)
    submitted_files = models.TextField(null='True')
    is_stale = models.BooleanField(default=True)

    def get_marks(self, section_type='Evaluate'):
        marks = 0
        for prgrm_result in ProgramResults.objects.filter(assignment_result=self):
            if prgrm_result.program.program_type == section_type:
                marks += prgrm_result.get_marks()
        return marks

# Model to store the results of a section. Used to manage section results.
# Stores the section, corresponding assignment result (consequently submission), compiler errors, output and return code.
class ProgramResults(models.Model):
    program = models.ForeignKey(Program)
    assignment_result = models.ForeignKey(AssignmentResults)
    missing_file_names = models.TextField(null='true')
    compiler_errors = models.TextField(null='true')
    compiler_output = models.TextField(null='true')
    compiler_return_code = models.IntegerField(null=True, blank=True)

    def get_marks(self):
        marks = 0
        for test_result in TestcaseResult.objects.filter(program_result=self):
            if test_result.test_passed:
                marks += test_result.test_case.marks
        return marks

def testcase_upload_path(instance, filename):
    assignment = instance.program.assignment
    return os.path.join(
                assignment.creater.username,
                assignment.course.title,
                assignment.name,
                'testcase-results',
                filename
            )

# Model to store results of testcases.
# Stores the testcase, program result (consequently submission and assignment), error message, return code, output and status for the testcase, 
class TestcaseResult(models.Model):
    test_case = models.ForeignKey(Testcase)
    program_result = models.ForeignKey(ProgramResults) # test_case and program_result will be unique in table.
    error_messages = models.TextField(null='true')
    return_code = models.IntegerField(null=True, blank=True)
    test_passed = models.BooleanField()
    output_files = models.FileField(upload_to='results/%Y/%m/%d', null='true')
signals.pre_delete.connect(delete_files, sender=TestcaseResult, dispatch_uid="delete_testcaseresults")