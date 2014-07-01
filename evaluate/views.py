from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import Http404
import os, tempfile

from assignments.models import Program as ProgramModel
from assignments.models import Assignment
from evaluate.models import AssignmentResults
from upload.models import Upload
from utils.evaluator import Evaluate, Results
from utils.checkOutput import CustomTestcase
from utils.errorcodes import error_codes, error_msg


# Function to evaluate a submission (passed as submissionID).
# Takes as input the request, submission ID, the section type (evaluate or practice), and the template page to which the response is to be rendered.
def evaluate(request, submissionID, program_type, template):
    submission = get_object_or_404(Upload, pk=submissionID)
    assignment = submission.assignment

    # Checking if the user sending the request is either the owner of the submission or the assignment creator (the only people authorized to evaluate).
    if not (request.user == submission.owner or request.user == assignment.creater):
        raise PermissionDenied

    # Checking if the user is a student. Checking if the assignment is past its due date.
    is_student = True if (request.user == submission.owner) else False
    is_due = (assignment.deadline <= timezone.now())

    # Evaluating the submission.
    current_dir = os.getcwd()
    try:
        results = Evaluate(submission).getResults(program_type=program_type)
    finally:
        os.chdir(current_dir)
    return render_to_response(
                template,
                {'submission': submission, 'assignment': assignment,
                'results': results, 'error_code': error_codes, 'is_student': is_student,
				'is_due': is_due, 'error_msg': error_msg},
                context_instance=RequestContext(request)
            )

# Function to evaluate an assignment submission. Called by either the student who submitted the solution or the instructor.
# Takes as input the submission ID and calls evaluate() function above appropriately.
@login_required
def evaluateAssignment(request, submissionID):
    '''Compile student's submission run all test cases and display results on html page.'''
    return evaluate(request, submissionID, "Evaluate", template='evaluate/results.html')

# Redundant function, but not removed so as to not break the code.
@login_required
def evaluateSubmission(request, submissionID):
    return evaluate(request, submissionID, "Evaluate", template='evaluate/results.html')

# Function that evaluates the result for custom input.
# Takes as input the section ID for which the testing is done with custom input.
@login_required
def checkOutput(request, programID):
    # Checking if the request method is POST
    if request.method == 'POST':
        temp_fname = ''
        # This stores the input text. If this is not present then a custom testcase file was uploaded (else).
        if request.POST.get('inputText'): 
            # Create a temporary file, and open it as inputFile variable. Read the custom testcase and store it in the file object.
            _, temp_fname = tempfile.mkstemp(prefix='user_input')
            inputFile = open(temp_fname, 'wb+')
            for a_char in request.POST.get('inputText'):
                inputFile.write(a_char)
            inputFile.close()
            inputFile = open(temp_fname)
        else:
            # If the custom testcase was not given in the text box, then a file was uploaded. It is read from the inputFile attribute of the request.
            inputFile = request.FILES.get('inputFile')

        # Get the section, assignment and the submission using the programID and user of the requestgiven as input.
        program = get_object_or_404(ProgramModel, pk=programID)
        assignment =  program.assignment
        submission = Upload.objects.get(owner=request.user, assignment=assignment)
        # TODO: Handle error if there was no submission.

        # Create a testcase object using the input file, the section and the submission. Get the results for this custom testcase.
        testcaseObject = CustomTestcase(inputFile, program, submission)
        old_pwd = os.getcwd()
        try:
            results = testcaseObject.getResult()
        finally:
            # Clear all temp files.
            if os.path.isfile(temp_fname):
                os.remove(temp_fname)
            os.chdir(old_pwd)
        return render_to_response(
                    'evaluate/customTestResults.html',
                    {'assignment': assignment, 'error_msg': error_msg,
                    'results': results, 'error_code': error_codes, 'program': program},
                    context_instance=RequestContext(request)
                )
    else:
        raise Http404

# Function to show results for a submission. This is different from the above functions in the sense that the other functions are called to evaluate
# a subsmission while this function is called to retrieve the results for a submission (already evaluated).
@login_required
def showResult(request, submissionID):
    # Retrieve the submission object and then retrieve the results of that submission using the Results class.
    submission = get_object_or_404(Upload, pk=submissionID)
    results = Results(submission, program_type="Evaluate")

    # If any results were found then render them.
    if results:
        assignment = submission.assignment
        is_student = True if (request.user == submission.owner) else False
        return render_to_response(
                'evaluate/results.html',
                {'submission': submission, 'assignment': assignment, 'error_msg': error_msg,
                'results': results, 'error_code': error_codes, 'is_student': is_student},
                context_instance=RequestContext(request)
            )

# Function to evaluate all submissions of an assignment.
# Takes as input the assignment ID for which all submissions needs to be evaluated.
@login_required
def eval_all_submissions(request, assignmentID):
    assignment = get_object_or_404(Assignment, pk=assignmentID)
    all_submissions = Upload.objects.filter(assignment=assignment)

    # Retrieve all the submissions for this assignment and evaluate them if the submission is stale.
    # Then redirect to upload_showAllSubmissions to take care of rendering the results.
    current_dir = os.getcwd()
    try:
        for submission in all_submissions:
            if not submission.is_stale:
                Evaluate(submission).eval(program_type="Evaluate")
    finally:
        os.chdir(current_dir)
    return HttpResponseRedirect(reverse('upload_showAllSubmissions', kwargs={'assignmentID': assignmentID}))

# Function to run practice testcases on the submission.
# Takes as input the submission ID and calls evaluate() function.
@login_required
def run_practice_test(request, submissionID):
    return evaluate(request, submissionID, "Practice", template='evaluate/practice_results.html')

# Function to evaluate submission and render a detailed table of results.
# Takes as input the submission ID and calls evaluate() function. The details of the results are rendered to evaluate/result_table.html.
@login_required
def evaluation_details(request, submissionID):
    return evaluate(request, submissionID, "Evaluate", template='evaluate/result_table.html')

# Function to retrieve the results of all submissions and render in a good format.
# Takes as input the assignment ID and gathers the results of all submissions.
@login_required
def complete_evaluation_details(request, assignmentID):
    # Gather the assigment object and then all submissions and section of this assignment.
    assignment=get_object_or_404(Assignment, pk=assignmentID)
    allSubmission = Upload.objects.filter(assignment=assignment)
    programs = ProgramModel.objects.filter(assignment=assignment, program_type="Evaluate")

    # For each submission get the results for all sections, and add to the allResults dictionary with the submission user as key.
    allResults = {}
    for submission in allSubmission:
        if not submission.is_stale:
            try:
                # Gather the results for the submission.
                results = Results(submission, program_type="Evaluate")
                program_result = {}
                # Retrieve the marks and submission ID for each section. This is all we need.
                for prgm_rslt in results.program_results :
                    program_result[prgm_rslt.program_result.program.name] = {'marks': prgm_rslt.marks, 'submissionId' : submission.id}
                allResults[submission.owner] = program_result
            except AssignmentResults.DoesNotExist:
                pass
    return render_to_response(
                'evaluate/students_result_table.html',
                {'assignment': assignment, 'allResults': allResults, 'programs': programs},
                context_instance=RequestContext(request)
            )