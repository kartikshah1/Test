'''
This file is not being used in any module
'''

from django.core.files.storage import default_storage
from django.core.files import File
from assignments.models import Program
from assignments.models import Testcase
from grader.settings import MEDIA_ROOT
import tarfile, os

class TestResults(object):
    def __init__(self, user):
        self.user = user

    def setSubmissionErrors(self):
        self.file_found = False
        self.compiled = False
        self.test_passed = False

    def setCompilationFailed(self, errorMessages):
        self.file_found = True
        self.compiled = False
        self.test_passed = False
        self.compiler_errors = errorMessages

    def setTestcaseFailed(self):
        self.file_found = True
        self.compiled = True
        self.test_passed = False

    def saveAssignmentResults(self, assignment):
        programs = Program.objects.filter(assignment=assignment)
        for program in programs:
            self.saveProgramResults(program)

    def saveProgramResults(self, program):
        testcases = Testcase.objects.filter(program=program)
        for testcase in testcases:
            self.saveTestcaseResults(testcase)

    def saveTestcaseResults(self, testcase, testResult=None):
        outputfiles = []
        if testcase.program.outputFiles:
            src = os.path.join(MEDIA_ROOT, testcase.program.outputFiles.name)
            tar = tarfile.open(src)
            outputfiles = [a.name for a in tar.getmembers() if a.isfile() and os.path.isfile(a.name)]
            tar.close()

        # Save results to database.
        testcaseResult, created = Results.objects.get_or_create(
                             user = self.user,
                             testcase = testcase
                             )
        testcaseResult.file_found = self.file_found if hasattr(self, 'file_found') else True
        testcaseResult.compiled = self.compiled if hasattr(self, 'compiled') else True
        testcaseResult.compiler_errors = "\n".join(self.compiler_errors) if hasattr(self, 'compiler_errors') else ""
        testcaseResult.test_passed = self.test_passed if hasattr(self, 'test_passed') else True
        
        if testResult is not None:
            testResult.runtime_errors = "\n".join(testResult.stderr)
        if not created:
            default_storage.delete(testcaseResult.output_files.path)

        testcaseResult.save()

        # Now add output-files to database. 
        stdoutFileName = "standardOutput_" + str(testcase.id)
        stdOutputofTestcase = open(stdoutFileName, 'w')

        if testResult is not None:
            stdOutputofTestcase.write("\n".join(testResult.stdout))
        stdOutputofTestcase.close()

        outputfiles.append(stdoutFileName)

        tarname = "output_file_" + str(testcase.id) + ".tar.bz2"
        outputFilesTar = tarfile.open(name=tarname, mode="w:bz2")

        for afile in outputfiles:
            outputFilesTar.add(afile)
        outputFilesTar.close()

        testcaseResult.output_files.save(tarname, File(open(tarname)) )
