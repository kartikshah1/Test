from assignments.models import Assignment, AssignmentErrors
from assignments.models import Program, ProgramErrors
from assignments.models import Testcase, TestcaseErrors, SafeExec
from evaluate.models import AssignmentResults
from upload.models import Upload
from assignments.forms import AssignmentForm
from assignments.forms import ProgramFormCNotE,ProgramFormE,ProgramFormCandE, SafeExecForm
from upload.forms import UploadForm
from grader.settings import MEDIA_ROOT
from utils.archives import get_file_name_list
from utils.filetypes import language_category, get_compiler_name, get_interpreter_name, get_compilation_command, get_execution_command

from django.db.models import Max
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.core.files.storage import default_storage
from django.contrib.formtools.wizard.views import SessionWizardView
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.forms import model_to_dict
from django.http import HttpResponseForbidden
from django.utils import timezone
from courseware.models import Course, CourseHistory, CourseInfo
from datetime import datetime
import os, pickle

from django.core.mail import send_mail

def isCourseCreator(course, user):
    course_history = CourseHistory.objects.get(course_id=course, user_id=user.id)
    return course_history.is_owner

def isCourseModerator(course, user):
    course_history = CourseHistory.objects.get(course_id=course, user_id=user.id)
    return course_history.is_owner or course_history.is_moderator

@login_required
def index(request, courseID):
    ''' List all assignments for courseID. courseID is automatically generated
    in Course table.'''
    course = get_object_or_404(Course, pk=courseID)
    all_assignments = Assignment.objects.filter(course=course).order_by('-serial_number')

    if CourseHistory.objects.filter(course_id=course, user_id=request.user.id).count() == 0:
        return HttpResponseForbidden("Forbidden 403")

    course_history = CourseHistory.objects.get(course_id=course, user_id=request.user.id)
    course_info = CourseInfo.objects.get(pk=course.course_info_id)
    is_creator = isCourseCreator(course, request.user)
    is_moderator = isCourseModerator(course, request.user)

    if is_moderator:
        assignments = all_assignments
        leave_course = False
        #number_of_students = Role.objects.filter(course=course).count()
        number_of_students = 0
    else:
        assignments = [a for a in all_assignments if a.publish_on <= timezone.now()]
        #leave_course = Role.objects.filter(user=request.user, course=course, role='S').count()
        leave_course = True
        number_of_students = 0
    return render_to_response(
                'assignments/index.html',
                {'assignments': assignments, 'is_moderator': is_moderator, 'course_info':course_info,
                 'date_time': timezone.now(),
                 'course': course, 'leave_course': bool(leave_course),
                 'number_of_students': number_of_students}, context_instance=RequestContext(request),
            )

@login_required
def deleteSubmission(request, uploadID):
    upload = get_object_or_404(Upload, pk=uploadID)
    if not request.user == upload.owner:
        return HttpResponseForbidden("Forbidden 403")

    assignmentID = upload.assignment.id
    upload.delete()
    return HttpResponseRedirect(reverse('assignments_details', kwargs={'assignmentID':assignmentID}))

@login_required
def detailsAssignment(request, assignmentID):
    assignment = get_object_or_404(Assignment, pk=assignmentID)
    course = assignment.course
    course_history = CourseHistory.objects.get(course_id=course, user_id=request.user.id)
    course_info = CourseInfo.objects.get(pk=course.course_info_id)
    is_creator = isCourseCreator(course, request.user)
    is_moderator = isCourseModerator(course, request.user)

    has_joined = CourseHistory.objects.filter(course_id=course, user_id=request.user.id)
    if assignment.late_submission_allowed:
        submission_allowed = (timezone.now() <= assignment.hard_deadline) and bool(has_joined)
    else:
        submission_allowed = (timezone.now() <= assignment.deadline) and bool(has_joined)

    is_due = (timezone.now() >= assignment.deadline)# and bool(has_joined)

    if request.method == "POST" and submission_allowed:
        form = UploadForm(request.POST, request.FILES, assignment_model_obj=assignment)
        if form.is_valid():
            older_upload = Upload.objects.filter(
                                owner=request.user,
                                assignment=assignment
                            )
            if older_upload:
                older_upload[0].delete()
            newUpload = Upload(
                            owner=request.user,
                            assignment=assignment,
                            filePath=request.FILES['docfile']
                        )
            newUpload.save()
            return HttpResponseRedirect(reverse('assignments_details', kwargs={'assignmentID':assignmentID}))
    else:
        form = UploadForm()

    perror_ctype = ContentType.objects.get_for_model(ProgramErrors)
    terror_ctype = ContentType.objects.get_for_model(TestcaseErrors)
    program_errors = []
    test_errors = []

    for error in AssignmentErrors.objects.filter(assignment=assignment, content_type=terror_ctype):
        test_errors.extend(TestcaseErrors.objects.filter(pk=error.object_id))

    for error in AssignmentErrors.objects.filter(assignment=assignment, content_type=perror_ctype):
        program_errors.extend(ProgramErrors.objects.filter(pk=error.object_id))


    course = assignment.course
    programs = Program.objects.filter(assignment=assignment)
    #test_cases = Testcase.objects.filter(program__in=programs)

    practice_program = [a_program for a_program in programs if a_program.program_type == "Practice"]
    programs_with_errors = []

    for aprogram in programs:
        if not aprogram.is_sane:
            try:
                p_error = ProgramErrors.objects.get(program=aprogram)
                programs_with_errors.append(p_error)
            except ProgramErrors.DoesNotExist:
                p_error = None

    submittedFiles = Upload.objects.filter(owner=request.user, assignment=assignment)
    
    program_not_ready = False
    disable_grading = False
    if programs_with_errors or submission_allowed == False:
    	program_not_ready = True
    if (submittedFiles and submittedFiles[0].is_stale) :
        disable_grading = True

    all_assignments = Assignment.objects.filter(course=course).order_by('-serial_number')
    if request.user == assignment.creater:
        assignments = all_assignments
    else:
        assignments = [a for a in all_assignments if a.publish_on <= timezone.now()]

    total_sumissions = Upload.objects.filter(assignment=assignment).count()
    isSubmitted = Upload.objects.filter(assignment=assignment).count() > 0
    get_params = {'source': 'assignment', 'id': assignmentID}

    return render_to_response(
                'assignments/details.html',
                {'assignment': assignment, 'course': course, 'has_joined': has_joined, 'is_moderator':is_moderator,
                'programs': programs, 'form': form, 'submission_allowed': submission_allowed,
                'submittedFiles': submittedFiles, 'programs_with_errors': programs_with_errors,
                'disable_grading': disable_grading, 'program_not_ready':program_not_ready, 'practice_program': practice_program,
                'assignments' : assignments, 'program_errors':program_errors, 'test_errors':test_errors,
                'published': assignment.publish_on <= timezone.now(), 'is_due': is_due,
                'isSubmitted':isSubmitted, 'date_time': timezone.now(), 'get_params': get_params,
                'total_sumissions': total_sumissions},
                context_instance=RequestContext(request),
            )

@login_required
def editAssignment(request, assignmentID):
    # Only creator of the course can edit this assignment.
    assignment = get_object_or_404(Assignment, pk=assignmentID)

    is_moderator = isCourseModerator(assignment.course, request.user)
    if not is_moderator:
        return HttpResponseForbidden("Forbidden 403")

    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES, initial=model_to_dict(assignment))
        form.assignment_model = assignment

        if form.is_valid():
            # check if new file is uploaded
            if 'document' in form.changed_data:
                if assignment.document:
                    assignment.document.delete(save=False)
                if not form.cleaned_data['document']:
                    form.cleaned_data.pop('document')

            if 'helper_code' in form.changed_data:
                if assignment.helper_code:
                    assignment.helper_code.delete(save=False)
                if not form.cleaned_data['helper_code']:
                    form.cleaned_data.pop('helper_code')

            if 'model_solution' in form.changed_data:
                if assignment.model_solution:
                    assignment.model_solution.delete(save=False)
                if not form.cleaned_data['model_solution']:
                    form.cleaned_data.pop('model_solution')

            for key in form.cleaned_data.keys():
                setattr(assignment, key, form.cleaned_data[key])

            for afield in ['model_solution', 'student_program_files', 'program_language']:
                if afield in form.changed_data:
                    assignment.verify_programs = True
                    assignment.program_model = Program
                    assignment.changed_list = form.changed_data
                    break
            assignment.save()

            if any(f in ['student_program_files', 'helper_code'] for f in form.changed_data):
                all_submissions = Upload.objects.select_related('owner').select_for_update().filter(assignment=assignment)
                all_submissions.update(is_stale=True)

                subject_line = "Evalpro: Please re-submit assignment '{0}' of the course '{1}'".format(assignment.name, assignment.course.name)
                message = "Course {0} assignment {1} specification has been changed since you submit your assignment last time. \
You are required to submit your assignment again. Your current submission will not be considered.".format(assignment.course.name, assignment.name)
                message_from = 'noreply@evalpro'
                message_to = [a.owner.email for a in all_submissions]
                send_mail(subject_line, message, message_from,
                          message_to, fail_silently=False)

            return HttpResponseRedirect(reverse('assignments_details', kwargs={'assignmentID':assignmentID}))
    else:
        form = AssignmentForm(initial=model_to_dict(assignment))

    course = assignment.course
    return render_to_response(
                'assignments/edit.html',
                {'assignment': assignment, 'form': form, 'course': course, 'is_moderator':is_moderator},
                context_instance=RequestContext(request),
            )

@login_required
def createAssignment(request, courseID):
    course = get_object_or_404(Course, pk=courseID)

    is_moderator = isCourseModerator(course, request.user)

    if not is_moderator:
        return HttpResponseForbidden("Forbidden 403")

    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        form.this_course = course
        if form.is_valid():
            newAssignment = Assignment(**form.cleaned_data)
            newAssignment.course = course
            newAssignment.creater = request.user
            newAssignment.serial_number = (Assignment.objects.filter(course=course).aggregate(Max('serial_number'))['serial_number__max'] or 0) + 1
            newAssignment.save()
            link = reverse('assignments_createprogram', kwargs={'assignmentID': newAssignment.id})
            messages.success(request, 'Assignment Created! Now <a href="{0}">ADD</a> programs to assignment.'.format(link),
                             extra_tags='safe'
                             )
            #return HttpResponseRedirect(reverse('assignments_index', kwargs={'courseID':courseID}))
            return HttpResponseRedirect(reverse('assignments_details', kwargs={'assignmentID': newAssignment.id}))
    else:
        form = AssignmentForm()
    return render_to_response(
                'assignments/createAssignment.html',
                {'form':form, 'course': course, 'is_moderator':is_moderator},
                context_instance=RequestContext(request)
            )

@login_required
def removeAssignment(request, assignmentID):
    assignment = get_object_or_404(Assignment, pk=assignmentID)
    course = assignment.course
    
    is_moderator = isCourseModerator(course, request.user)
    if not is_moderator:
        return HttpResponseForbidden("Forbidden 403")

    assignment.delete()
    return HttpResponseRedirect(reverse('assignments_index', kwargs={'courseID': course.id}))

@login_required
def createProgram(request, assignmentID):
    assignment = get_object_or_404(Assignment, pk=assignmentID)
    course = assignment.course
    # Only creator of course can create new program in assignment.

    is_moderator = isCourseModerator(course, request.user)
    if not is_moderator:
        return HttpResponseForbidden("Forbidden 403")

    if request.method == 'POST':
        lang_category = language_category(assignment.program_language)
        if(lang_category == 0): #Compilation needed. Execution not needed. C and C++
            form = ProgramFormCNotE(request.POST, request.FILES)
        elif(lang_category == 1): #Compilation and execution needed.
            form = ProgramFormCandE(request.POST, request.FILES)
        elif(lang_category == 2): #Execution needed. Python and bash
            form = ProgramFormE(request.POST, request.FILES)
        form.assignment = assignment # files submitted by student
        if form.is_valid():
            newProgram = Program(**form.cleaned_data)
            newProgram.assignment = assignment
            newProgram.is_sane = True
            newProgram.compile_now = True
            newProgram.execute_now = True
            newProgram.language = assignment.program_language
            newProgram.save()
            link = reverse('assignments_createtestcase', kwargs={'programID': newProgram.id})
            messages.success(request, 'Section Created! Now <a href="{0}">ADD</a> testcase for this program.'.format(link),
                             extra_tags='safe'
                             )
            all_submissions = Upload.objects.filter(assignment=assignment)
            AssignmentResults.objects.filter(submission__in=all_submissions).update(is_stale=True)
            return HttpResponseRedirect(reverse('assignments_details', kwargs={'assignmentID':assignmentID}))
    else:
        objs = Program.objects.filter(assignment=assignment)
        initial = {}
        lang_category = language_category(assignment.program_language)
        if objs:
            if lang_category == 0:
                comp_command = pickle.loads(objs[0].compiler_command)
                initial['compiler_command'] = pickle.dumps([comp_command[0], '', ''])
            elif lang_category == 1:
                comp_command = pickle.loads(objs[0].compiler_command)
                initial['compiler_command'] = pickle.dumps([comp_command[0], '', ''])
                exe_command = pickle.loads(objs[0].execution_command)
                initial['execution_command'] = pickle.dumps([exe_command[0], '', ''])
            elif lang_category == 2:
                exe_command = pickle.loads(objs[0].execution_command)
                initial['execution_command'] = pickle.dumps([exe_command[0], '', ''])
        else:
            if lang_category == 0:
                comp_command = get_compiler_name(assignment.program_language)
                initial['compiler_command'] = pickle.dumps([comp_command, '', ''])
            elif lang_category == 1:
                comp_command = get_compiler_name(assignment.program_language)
                initial['compiler_command'] = pickle.dumps([comp_command, '', ''])
                exe_command = get_interpreter_name(assignment.program_language)
                initial['execution_command'] = pickle.dumps([exe_command, '', ''])
            elif lang_category == 2:
                exe_command = get_interpreter_name(assignment.program_language)
                initial['execution_command'] = pickle.dumps([exe_command, '', ''])
        if lang_category == 0 : #Compilation needed. Execution not needed. C and C++
            form = ProgramFormCNotE(initial=initial)
        elif lang_category == 1 : #Compilation and execution needed.
            form = ProgramFormCandE(initial=initial)
        elif lang_category == 2 : #Execution needed. Python and bash
            form = ProgramFormE(initial=initial)

    course = assignment.course
    return render_to_response(
                'assignments/createProgram.html',
                {'form':form, 'assignment': assignment, 'course': course, 'is_moderator':is_moderator},
                context_instance=RequestContext(request)
            )

@login_required
def editProgram(request, programID):
    program = get_object_or_404(Program, pk=programID)
    is_moderator = isCourseModerator(program.assignment.course, request.user)
    if not is_moderator:
        return HttpResponseForbidden("Forbidden 403")

    if request.method == 'POST':
        # form is initialized by model then overwritten by request data and files.
        lang_category = language_category(program.assignment.program_language)
        if(lang_category == 0): #Compilation needed. Execution not needed. C and C++
            form = ProgramFormCNotE(request.POST, request.FILES, initial=model_to_dict(program))
        elif(lang_category == 1): #Compilation and execution needed.
            form = ProgramFormCandE(request.POST, request.FILES, initial=model_to_dict(program))
        elif(lang_category == 2): #Execution needed. Python and bash
            form = ProgramFormE(request.POST, request.FILES, initial=model_to_dict(program))
        form.assignment = program.assignment
        form.program_model = program
        if form.is_valid():
            # check if new file is uploaded
            if 'program_files' in form.changed_data: # program_files are changed."
                if program.program_files: # delete older file if any.
                    program.program_files.delete(save=False)
                if not form.cleaned_data['program_files']: # if file is being cleared.
                    form.cleaned_data.pop('program_files')

            if 'makefile' in form.changed_data:
                if program.makefile:
                    program.makefile.delete(save=False)
                if not form.cleaned_data['makefile']:
                    form.cleaned_data.pop('makefile')

            for key in form.cleaned_data.keys():
                setattr(program, key, form.cleaned_data[key])

            program.delete_error_message()
            program.is_sane = True
            for afield in ['program_files', 'compiler_command', 'makefile', 'execution_command']:
                if afield in form.changed_data:
                    program.compile_now = True
                    program.execute_now = True
                    break
            program.save()

            # Mark all assignment results to stale if either program_files or compiler_command or execution_command have changed
            changed_fields = ['program_files']
            if program.compiler_command:
                changed_fields.append('compiler_command')
            if program.execution_command:
                changed_fields.append('execution_command')
            if set(changed_fields) - set(form.changed_data):
                all_submissions = Upload.objects.filter(assignment=program.assignment)
                AssignmentResults.objects.filter(submission__in=all_submissions).update(is_stale=True)

            return HttpResponseRedirect(reverse('assignments_detailsprogram', kwargs={'programID':programID}))
    else:
        lang_category = language_category(program.assignment.program_language)
        if(lang_category == 0): #Compilation needed. Execution not needed. C and C++
            form = ProgramFormCNotE(initial=model_to_dict(program))
        elif(lang_category == 1): #Compilation and execution needed.
            form = ProgramFormCandE(initial=model_to_dict(program))
        elif(lang_category == 2): #Execution needed. Python and bash
            form = ProgramFormE(initial=model_to_dict(program))

    return render_to_response(
                'assignments/editProgram.html',
                {'form':form, 'program': program},
                context_instance=RequestContext(request)
            )

@login_required
def detailProgram(request, programID):
    program = get_object_or_404(Program, pk=programID)
    testcases = Testcase.objects.filter(program=program)
    assignment = program.assignment
    is_due = (timezone.now() >= assignment.deadline)
    course = assignment.course
    has_submitted = Upload.objects.filter(owner=request.user, assignment=assignment)
    all_assignments = Assignment.objects.filter(course=course).order_by('-serial_number')
    
    is_moderator = isCourseModerator(course, request.user)
    if is_moderator:
        assignments = all_assignments
    else:
        assignments = [a for a in all_assignments if a.publish_on <= timezone.now()]
    compiler_command = get_compilation_command(program)
    execution_command = get_execution_command(program)
    program_errors = None
    if not program.is_sane:
        try:
            program_errors = ProgramErrors.objects.get(program=program)
        except ProgramErrors.DoesNotExist:
            program_errors = None
    testcase_errors = []
    terror_ctype = ContentType.objects.get_for_model(TestcaseErrors)
    for error in AssignmentErrors.objects.filter(assignment=program.assignment, content_type=terror_ctype):
        testcase_errors.extend(TestcaseErrors.objects.filter(pk=error.object_id))
    get_params = {'source': 'section', 'id': programID}
    return render_to_response(
                'assignments/detailsProgram.html',
                {'program':program, 'testcases':testcases, 'assignment':assignment,
                 'assignments':assignments, 'date_time': timezone.now(),
                 'program_errors':program_errors, 'compiler_command':compiler_command, 'execution_command':execution_command, 'course':course, 'is_moderator':is_moderator,
                 'is_due': is_due, 'has_submitted':has_submitted, 'get_params': get_params,
                 'testcase_errors': testcase_errors},
                context_instance=RequestContext(request)
            )

@login_required
def removeProgram(request, programID):
    program = get_object_or_404(Program, pk=programID)
    is_moderator = isCourseModerator(program.assignment.course, request.user)
    if not is_moderator:
        return HttpResponseForbidden("Forbidden 403")

    assignment = program.assignment
    program.delete()
    return HttpResponseRedirect(reverse('assignments_details', kwargs={'assignmentID':assignment.id}))

class CreateTestcaseWizard(SessionWizardView):
    file_storage = default_storage
    template_name = 'assignments/createTestcasewizard.html'

    def dispatch(self, request, *args, **kwargs):
        program_id = kwargs['programID']
        program = get_object_or_404(Program, pk=program_id)
        # self.solution_ready is used in from clean method.
        if Testcase.objects.filter(program=program):
        	self.solution_ready = program.solution_ready
        else:
            self.solution_ready = bool(program.program_files or program.assignment.model_solution)

        is_moderator = isCourseModerator(program.assignment.course, request.user)
        if is_moderator:
            return super(CreateTestcaseWizard, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Forbidden 403")

    def get_form_kwargs(self, step=None):
        if step == '0':
            return {'solution_ready' : self.solution_ready}
        if step == '1':
            choice_dict = {}
            if self.storage.get_step_files('0'):
                if self.storage.get_step_files('0').get('0-input_files', ""):
                    f_in_obj = self.storage.get_step_files('0').get('0-input_files')
                    f_in_obj.open()
                    choice_dict['in_file_choices'] = [(a, a) for a in get_file_name_list(fileobj=f_in_obj)]

                if self.storage.get_step_files('0').get('0-output_files', ""):
                    f_out_obj = self.storage.get_step_files('0').get('0-output_files')
                    f_out_obj.open()
                    choice_dict['out_file_choices'] = [(b, b) for b in get_file_name_list(fileobj=f_out_obj)]
            return choice_dict
        else:
            return super(CreateTestcaseWizard, self).get_form_kwargs(step)

    def get_context_data(self, form, **kwargs):
        context = super(CreateTestcaseWizard, self).get_context_data(form=form, **kwargs)

        program = Program.objects.get(pk=self.kwargs['programID'])
        compiler_command = get_compilation_command(program)
        execution_command = get_execution_command(program)
        context.update({'program': program, 'compiler_command': compiler_command, 'execution_command':execution_command})
        return context

    def done(self, form_list, **kwargs):
        frmdict = form_list[0].cleaned_data
        frmdict.update(form_list[1].cleaned_data)
        program = Program.objects.get(pk=self.kwargs['programID'])
        frmdict.update({'program': program})

        Testcase.objects.create(**frmdict)

        # Remove temporary files
        if self.storage.get_step_files('0'):
            for a in self.storage.get_step_files('0').values():
                try:
                    os.remove(os.path.join(MEDIA_ROOT, a.name))
                except Exception:
                        pass

        all_submissions = Upload.objects.filter(assignment=program.assignment)
        AssignmentResults.objects.filter(submission__in=all_submissions).update(is_stale=True)
        return HttpResponseRedirect(reverse('assignments_detailsprogram', kwargs={'programID': self.kwargs['programID']}))


class EditTestcaseWizard(SessionWizardView):
    file_storage = default_storage
    template_name = 'assignments/editTestcasewizard.html'

    def dispatch(self, request, *args, **kwargs):
        testcase_id = kwargs['testcaseID']
        testcase = get_object_or_404(Testcase, pk=testcase_id)
        program = testcase.program
        # self.solution_ready is used in from clean method.
        self.solution_ready = bool(program.program_files or program.assignment.model_solution)
        is_moderator = isCourseModerator(program.assignment.course, request.user)
        if is_moderator:
            return super(EditTestcaseWizard, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("Forbidden 403")

    def get_form_initial(self, step):
        testcase = Testcase.objects.get(pk=self.kwargs['testcaseID'])
        return model_to_dict(testcase)

    def get_form_kwargs(self, step=None):
        if step == '0':
            return {'solution_ready' : self.solution_ready}
        if step == '1':
            choice_dict = {}
            testcase = Testcase.objects.get(pk=self.kwargs['testcaseID'])
            if self.storage.get_step_files('0'): # if there is at least one file.
                if self.storage.get_step_files('0').get('0-input_files', ""): # if input_file is uploaded.
                    f_in_obj = self.storage.get_step_files('0').get('0-input_files')
                    f_in_obj.open()
                    choice_dict['in_file_choices'] = [(a, a) for a in get_file_name_list(fileobj=f_in_obj)]
                elif testcase.input_files: # provide options from older file.
                    choice_dict['in_file_choices'] = [(b, b) for b in get_file_name_list(fileobj=testcase.input_files.file)]

                if self.storage.get_step_files('0').get('0-output_files', ""): # if output_file is uploaded.
                    f_out_obj = self.storage.get_step_files('0').get('0-output_files')
                    f_out_obj.open()
                    choice_dict['out_file_choices'] = [(b, b) for b in get_file_name_list(fileobj=f_out_obj)]
                elif testcase.output_files: # provide options from older file.
                    choice_dict['out_file_choices'] = [(b, b) for b in get_file_name_list(fileobj=testcase.output_files.file)]

            else: # No file uploaded in step 0
                if '0-input_files-clear' not in self.storage.get_step_data('0') and testcase.input_files:
                    choice_dict['in_file_choices'] = [(b, b) for b in get_file_name_list(fileobj=testcase.input_files.file)]
                else:
                    pass
                if '0-output_files-clear' not in self.storage.get_step_data('0') and testcase.output_files:
                    choice_dict['out_file_choices'] = [(b, b) for b in get_file_name_list(fileobj=testcase.output_files.file)]
            return choice_dict
        else:
            return super(EditTestcaseWizard, self).get_form_kwargs(step)

    def get_context_data(self, form, **kwargs):
        context = super(EditTestcaseWizard, self).get_context_data(form=form, **kwargs)

        testcase = Testcase.objects.get(pk=self.kwargs['testcaseID'])
        program = testcase.program
        compiler_command = get_compilation_command(program)
        execution_command = get_execution_command(program)
        context.update({'testcase': testcase, 'compiler_command': compiler_command, 'execution_command':execution_command})
        return context

    def done(self, form_list, **kwargs):
        frmdict = form_list[0].cleaned_data
        frmdict.update(form_list[1].cleaned_data) # consolidated list from both steps.
        testcase = Testcase.objects.get(pk=self.kwargs['testcaseID'])

        if 'input_files' in form_list[0].changed_data: # either new file is being uploaded or older is cleared
            if testcase.input_files: # there was an older file in test-case
                testcase.input_files.delete(save=False) # delete older file.
            if not form_list[0].cleaned_data['input_files']: # no new file so do nothing
                form_list[0].cleaned_data.pop('input_files')

        if 'output_files' in form_list[0].changed_data:
            if testcase.output_files:
                testcase.output_files.delete(save=False)
            if not form_list[0].cleaned_data['output_files']:
                form_list[0].cleaned_data.pop('output_files')

        for key in frmdict.keys(): # update database table row.
                setattr(testcase, key, frmdict[key])
        testcase.save()

        files_change = set(['input_files', 'output_files']) - set(form_list[0].changed_data)
        stdIO_change = set(['std_in_file_name', 'std_out_file_name']) - set(form_list[1].changed_data)
        if files_change or stdIO_change:
            testcase = Testcase.objects.get(pk=self.kwargs['testcaseID'])
            all_submissions = Upload.objects.filter(assignment=testcase.program.assignment)
            AssignmentResults.objects.filter(submission__in=all_submissions).update(is_stale=True)

        # Remove temporary files
        if self.storage.get_step_files('0'):
            for a in self.storage.get_step_files('0').values():
                try:
                    os.remove(os.path.join(MEDIA_ROOT, a.name))
                except Exception:
                    pass
        return HttpResponseRedirect(reverse('assignments_detailstestcase', kwargs={'testcaseID': self.kwargs['testcaseID']}))


@login_required
def detailTestcase(request, testcaseID):
    testcase = get_object_or_404(Testcase, pk=testcaseID)
    course = testcase.program.assignment.course
    all_assignments = Assignment.objects.filter(course=course).order_by('-serial_number')
    is_moderator = isCourseModerator(course, request.user)
    if is_moderator:
        assignments = all_assignments
    else:
        assignments = [a for a in all_assignments if a.publish_on <= timezone.now()]
    is_due = (timezone.now() >= testcase.program.assignment.deadline)
    get_params = {'source': 'testcase', 'id': testcaseID}
    testcase_errors = TestcaseErrors.objects.filter(testcase=testcase)
    return render_to_response(
                'assignments/detailsTestcase.html',
                {'testcase': testcase, 'assignments': assignments, 'date_time': timezone.now(),
                 'course': course, 'is_due': is_due, 'is_moderator':is_moderator,
                 'testcase_errors': testcase_errors, 'get_params': get_params},
                context_instance=RequestContext(request)
            )

@login_required
def removeTestcase(request, testcaseID):
    testcase = get_object_or_404(Testcase, pk=testcaseID)
    course = testcase.program.assignment.course
    is_moderator = isCourseModerator(course, request.user)
    if not is_moderator:
        return HttpResponseForbidden("Forbidden 403")

    program = testcase.program
    testcase.delete()
    return HttpResponseRedirect(reverse('assignments_detailsprogram', kwargs={'programID': program.id}))

@login_required
def config_safeexec_params(request, assignmentID):
    assignment = get_object_or_404(Assignment, pk=assignmentID)
    if not request.user == assignment.course.creater:
        return HttpResponseForbidden("Forbidden 403")

    if request.method == 'POST':
        form = SafeExecForm(request.POST)
        source = request.POST.get('page_source', '')
        test_ids = request.POST.getlist('testcases_cbx')
        if form.is_valid():
            for test_id in test_ids:
                testcase_obj = get_object_or_404(Testcase, pk=test_id)
                obj = SafeExec.objects.filter(testcase=testcase_obj)

                if len(obj) != 0:
                    form.cleaned_data['testcase'] = testcase_obj
                    obj.update(**form.cleaned_data)
                else:
                    form.cleaned_data['testcase'] = testcase_obj
                    SafeExec.objects.create(**form.cleaned_data)

            return HttpResponseRedirect(reverse('assignments_details', kwargs={'assignmentID':assignmentID}))
    else:
        default_limits = {'cpu_time':10, 'clock_time':60,
                          'memory':32768, 'stack_size':8192,
                          'child_processes':0, 'open_files':512,
                           'file_size':1024,}
        form = SafeExecForm(initial=default_limits)
        source = request.GET.get('source', '')
    if source == "section":
        section_id = request.GET.get('id', '')
        program = get_object_or_404(Program, pk=section_id)
        test_cases = Testcase.objects.filter(program=program)
        title = program.name
    elif source == "testcase":
        testcase_id = request.GET.get('id', '')
        test_cases = get_object_or_404(Testcase, pk=testcase_id)
        title = test_cases.name
    else:
        programs = Program.objects.filter(assignment=assignment).order_by('name')
        test_cases = []
        for a_program in programs:
            test_cases.append(Testcase.objects.filter(program=a_program).order_by('name'))
            #Testcase.objects.filter(program__in=programs)
        title = assignment.name

    return render_to_response(
                'assignments/safeexec_params.html',
                {'form': form, 'testcases': test_cases, 'source': source, 'title': title, 'assignment': assignment},
                context_instance=RequestContext(request)
            )

@login_required
def programList(request):
    data = ''
    if request.is_ajax():
        if request.method == 'GET':
            assignmentID = request.GET['asgnid']
            assignment = get_object_or_404(Assignment, pk=assignmentID)
            programs = Program.objects.filter(assignment=assignment).order_by('-program_type', 'id')
            if programs:
                for program in programs:
                    link = reverse('assignments_detailsprogram', kwargs={'programID': program.id})
                    data = data + '<li><label class="tree-toggler nav-header programs" id="p' + str(program.id) + '">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</label>'
                    data = data + '<a href="{0}">' + program.name + ' (' + program.program_type + ')' + '</a><div class="cb"></div>'
                    data = data + '<input type="hidden" class="progid" value="' + str(program.id) + '" />'
                    data = data + '<input type="hidden" class="loaded-testcases" value="0" />'
                    data = data + '<ul class="nav nav-list tree">'
                    data = data + '</ul>'
                    data = data + '</li>'
                    data = data.format(link)
            else:
                data = '<li style="font-size: 12px;">No programs for this assignment</li>'
        else:
            data = 'Error occurred'
    else:
        data = 'Error occurred'
    return HttpResponse(data)

@login_required
def testcaseList(request):
    data = ''
    if request.is_ajax():
        if request.method == 'GET':
            programID = request.GET['progid']
            program = get_object_or_404(Program, pk=programID)
            testcases = Testcase.objects.filter(program=program).order_by('id')
            if testcases:
                for testcase in testcases:
                    link = reverse('assignments_detailstestcase', kwargs={'testcaseID': testcase.id})
                    data = data + '<li><a href="{0}">&nbsp;&nbsp;' + testcase.name + '</a></li>'
                    data = data.format(link)
            else:
                data = '<li style="font-size: 12px;">No testcases for this program</li>'
        else:
            data = 'Error occurred'
    else:
        data = 'Error occurred'
    return HttpResponse(data)