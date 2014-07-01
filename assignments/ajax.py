from assignments.models import Assignment
from assignments.models import Program
from assignments.models import Testcase
from evaluate.models import ProgramResults
from evaluate.models import TestcaseResult
from upload.models import Upload

from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register

from utils.archives import archive_filepaths, extract_or_copy_singlefile

import shutil, tempfile

@dajaxice_register
def getfilesUploaded(request, submissionID):
    submission = get_object_or_404(Upload, pk=submissionID)
    assignment = submission.assignment

    if not (request.user == submission.owner or request.user == assignment.creater):
        raise PermissionDenied

    src = submission.filePath.file.name # gives absolute path
    submittedFiles = archive_filepaths(name=src)

    dajax = Dajax()

#    htmldata = ""
    popupdata = ''
    for submittedFile in submittedFiles:
#        htmldata += '<a href = "javascript:loadfile(' + str(submissionID) + ',\'' + submittedFile  + '\');">' + submittedFile + '</a>,'
        popupdata += '<li style="text-align:center;"><a href = "javascript:loadfile(' + str(submissionID) + ',\'' + submittedFile  + '\');">' + submittedFile + '</a></li>'
        popupdata += '<li class="divider"></li>'

#    dajax.clear('#filelist', 'innerHTML')
#    dajax.append('#filelist','innerHTML',htmldata)

    dajax.clear('.popup-data-files', 'innerHTML')
    dajax.append('.popup-data-files','innerHTML',popupdata)
    return dajax.json()

@dajaxice_register
def loadFile(request, submissionID, filePath):
    submission = get_object_or_404(Upload, pk=submissionID)
    assignment = submission.assignment

    if not (request.user == submission.owner or request.user == assignment.creater):
        raise PermissionDenied

    src = submission.filePath.file.name # gives absolute path
    temp_dir = tempfile.mkdtemp(prefix="grader")
    filedata = ''
    try:
        extract_or_copy_singlefile(src, temp_dir, filePath)

        #reading file data and storing it as a string
        temp_file_path = temp_dir + "/" + filePath
        print temp_file_path

        filePtr = open(temp_file_path, 'r')
        for line in filePtr:
            filedata += line

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

    dajax = Dajax()
    dajax.assign('#filedata', 'value', filedata)
    return dajax.json()

@dajaxice_register
def loadStats(request, assignmentID):
    assignment = get_object_or_404(Assignment, pk=assignmentID)
    programs = Program.objects.filter(assignment=assignment)

    numSubmissions = Upload.objects.filter(assignment=assignment).count()
    statsTable = "<div style='text-align:center;'><b>Total Number of submissions : " + str(numSubmissions) + "</b></div><br />"
    statsTable += "<table class='table table-bordered'><thead><tr><th>Section Name</th><th>Compilation Errors</th><th>Testcase Name</th><th>Failed this testcase</th></tr></thead><tbody>"
    for aprogram in programs:
        numCompErrors = ProgramResults.objects.filter(program=aprogram, compiler_return_code=1).count()
        testcases = Testcase.objects.filter(program=aprogram)
        if testcases.__len__() == 0:
            statsTable += "<tr>"
            statsTable += "<td>" + aprogram.name + "</td>"
            statsTable += "<td>" + str(numCompErrors) + "</td>"
            statsTable += "<td></td>"
            statsTable += "<td></td>"
            statsTable += "</tr>"
        else:
            statsTable += "<tr>"
            statsTable += "<td rowspan='" + str(testcases.__len__()) + "'>" + aprogram.name + "</td>"
            statsTable += "<td rowspan='" + str(testcases.__len__()) + "'>" + str(numCompErrors) + "</td>"
            i = 0
            for atestcase in testcases:
                failedTestcases = TestcaseResult.objects.filter(test_case=atestcase, test_passed=False).count()
                if i == 0:
                    i += 1
                    statsTable += "<td>" + atestcase.name + "</td>"
                    statsTable += "<td>" + str(failedTestcases) + "</td>"
                    statsTable += "</tr>"
                else:
                    i += 1
                    statsTable += "<tr>"
                    statsTable += "<td>" + atestcase.name + "</td>"
                    statsTable += "<td>" + str(failedTestcases) + "</td>"
                    statsTable += "</tr>"
    statsTable += "</tbody></table>"
            
    dajax = Dajax()
    dajax.clear('#stats', 'innerHTML')
    dajax.append('#stats','innerHTML',statsTable)
    return dajax.json()