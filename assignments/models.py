from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models.signals import post_save, pre_delete, pre_save
from django.core.files import File
import os, tempfile
from decimal import Decimal

#from courses.models import Course
from courseware.models import Course
from assignments import receivers

def assignment_upload_path(instance, filename):
    return os.path.join(
                instance.creater.username,
                instance.course.title,
                tempfile.mktemp().split('/')[-1],
                filename
            )

class Assignment(models.Model):
    course = models.ForeignKey(Course)
    name = models.CharField(max_length=200)
    serial_number = models.IntegerField()
    program_language = models.CharField(max_length=32)
    deadline = models.DateTimeField(null='true')
    hard_deadline = models.DateTimeField(null='true')
    publish_on = models.DateTimeField()
    late_submission_allowed = models.BooleanField(default=False)
    document = models.FileField(upload_to=assignment_upload_path, null='true')
    helper_code = models.FileField(upload_to=assignment_upload_path, null='true')
    model_solution = models.FileField(upload_to=assignment_upload_path, null='true')
    student_program_files = models.CharField(max_length=1024) # files that student must submit
    description = models.TextField(null='true')

    creater = models.ForeignKey(User)
    createdOn = models.DateTimeField(auto_now_add=True)
    last_modified_on = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("course", "name")
pre_delete.connect(receivers.delete_files, sender=Assignment, dispatch_uid="delete_assignment")
post_save.connect(receivers.verify_all_programs, sender=Assignment, dispatch_uid="receivers_verify_all_programs")


class AssignmentErrors(models.Model):
    assignment = models.ForeignKey(Assignment)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')


''' An assignment can have multiple programs. This table stores all
parameters to compile all programs for an assignment. '''
def program_upload_path(instance, filename):
    return os.path.join(
                instance.assignment.creater.username,
                instance.assignment.course.title,
                instance.assignment.name,
                'program-files',
                tempfile.mktemp().split('/')[-1],
                filename
            )

class Program(models.Model):
    assignment = models.ForeignKey(Assignment)
    name = models.CharField(max_length=128)
    program_type = models.CharField(max_length=10)
    compiler_command = models.CharField(max_length=1024)
    execution_command = models.CharField(max_length=1024,default='')
    program_files = models.FileField(upload_to=program_upload_path, null='true') # source code given by instructor.
    makefile = models.FileField(upload_to=program_upload_path, null='true')
    description = models.TextField(null='true')
    is_sane = models.BooleanField(default=True)
    language = models.CharField(max_length=32)
    solution_ready = models.BooleanField(default=True)

    def save_error(self, message): # remember it will also save current program object.
        post_save.disconnect(receivers.compile_solution, sender=Program, dispatch_uid="Compile_solution_program")
        self.is_sane = False
        self.save()
        p_errors, created = ProgramErrors.objects.get_or_create(program=self, defaults={'error_message': message})
        if not created:
            p_errors.error_message = message
            p_errors.save()
        post_save.connect(receivers.compile_solution, sender=Program, dispatch_uid="Compile_solution_program")

        ctype = ContentType.objects.get_for_model(ProgramErrors)
        AssignmentErrors.objects.get_or_create(
                                    content_type=ctype,
                                    object_id=p_errors.id,
                                    assignment=self.assignment
                                )

    def set_sane(self):
        post_save.disconnect(receivers.compile_solution, sender=Program, dispatch_uid="Compile_solution_program")
        self.is_sane = True
        self.save()
        post_save.connect(receivers.compile_solution, sender=Program, dispatch_uid="Compile_solution_program")

    def delete_error_message(self):
        try:
            program_error = ProgramErrors.objects.filter(program=self)[0:1].get()
            # delete entry from assignment error.
            ctype = ContentType.objects.get_for_model(ProgramErrors)
            AssignmentErrors.objects.filter(content_type=ctype, object_id=program_error.id).delete()
            program_error.delete()
        except ProgramErrors.DoesNotExist:
            pass
        except AssignmentErrors.DoesNotExist:
            pass

        #if program_error:
        #    program_error[0].delete()

    # Updates the output files of all testcases. Deleting older files will result in a call to model's save method 
    # which in turn will call pre_save method.
    def UpdateOutput(self):
        print "Inside UpdateOutput - Updating the outputs of all the testcases"
        post_save.disconnect(receivers.compile_solution, sender=Program, dispatch_uid="Compile_solution_program")
        all_tests = Testcase.objects.filter(program=self)
        for a_test in all_tests:
            a_test.output_files.delete()
        post_save.connect(receivers.compile_solution, sender=Program, dispatch_uid="Compile_solution_program")

post_save.connect(receivers.compile_solution, sender=Program, dispatch_uid="Compile_solution_program")
pre_delete.connect(receivers.delete_files, sender=Program, dispatch_uid="delete_program")

class ProgramErrors(models.Model):
    program = models.ForeignKey(Program)
    error_message = models.CharField(max_length=4096)

def testcase_upload_path(instance, filename):
    assignment = instance.program.assignment
    return os.path.join(
                assignment.creater.username,
                assignment.course.title,
                assignment.name,
                'testcase-files',
                tempfile.mktemp().split('/')[-1],
                filename
            )

class Testcase(models.Model):
    program = models.ForeignKey(Program)
    command_line_args = models.TextField(null='true')
    name = models.CharField(max_length=128)
    marks = models.IntegerField(null='true')
    input_files = models.FileField(upload_to=testcase_upload_path)
    output_files = models.FileField(upload_to=testcase_upload_path)
    std_in_file_name = models.CharField(max_length=256) # stores relative(to temp directory) path of the file.
    std_out_file_name = models.CharField(max_length=256) # stores relative(to temp directory) path of the file.
    description = models.TextField(null='true')

    def save_error(self, error_file):
        filter_attrs = {'testcase': self}
        attrs = {'error_message': "".join(open(error_file))}
        try:
            obj = TestcaseErrors.objects.filter(**filter_attrs)
            obj.update(**attrs)
            testcase_error = obj[0:1].get()
        except TestcaseErrors.DoesNotExist:
            attrs.update(filter_attrs)
            testcase_error = TestcaseErrors.objects.create(**attrs)
            # make an entry in assignment error.
        ctype = ContentType.objects.get_for_model(TestcaseErrors)
        AssignmentErrors.objects.get_or_create(
                                    content_type=ctype,
                                    object_id=testcase_error.id,
                                    assignment=self.program.assignment
                                )

    def clear_error(self):
        try:
            testcase_error = TestcaseErrors.objects.filter(testcase=self)[0:1].get()
            # delete entry from assignment error.
            ctype = ContentType.objects.get_for_model(TestcaseErrors)
            tmp_obj = AssignmentErrors.objects.filter(content_type=ctype, object_id=testcase_error.id)#.delete()

            tmp_obj.delete()
            testcase_error.delete()
        except TestcaseErrors.DoesNotExist:
            pass

pre_delete.connect(receivers.delete_files, sender=Testcase, dispatch_uid="delete_testcase")
pre_save.connect(receivers.create_op_files, sender=Testcase, dispatch_uid="create_output_files")
post_save.connect(receivers.testcase_cleanup, sender=Testcase, dispatch_uid="testcase_cleanup")



class TestcaseErrors(models.Model):
    testcase = models.ForeignKey(Testcase, unique=True)
    error_message = models.TextField(null='true')

class SafeExec(models.Model):
    testcase = models.ForeignKey(Testcase, unique=True)
    cpu_time = models.IntegerField()
    clock_time = models.IntegerField()
    memory = models.IntegerField()
    stack_size = models.IntegerField()
    child_processes = models.IntegerField()
    open_files = models.IntegerField()
    file_size = models.IntegerField()
    env_vars = models.TextField(null='true')