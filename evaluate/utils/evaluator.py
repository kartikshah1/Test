from grader.settings import PROJECT_ROOT
from evaluate.models import AssignmentResults
from evaluate.models import ProgramResults
from evaluate.models import TestcaseResult
from assignments.models import Testcase
from assignments.models import Program as ProgramModel
from evaluate.utils.executor import CommandExecutor
from utils.archives import get_file_name_list, extract_or_copy, read_file
from utils.filetypes import COMPILED_LANGUAGES, INTERPRETED_LANGUAGES, compile_required, get_execution_command, get_compilation_command

from django.core.files import File
from django.core.files.storage import default_storage
import os, shutil, tarfile, pickle, tempfile


# Class to manage execution of student submission on a testcase.
# The class members are the testcase, the program result of the section, the name of the testcase, the input file of the testcase, and a command executor.
class TestCase(object):
    def __init__(self, testcase, program_result):
        self.testcase = testcase
        self.program_result = program_result
        self.name = testcase.name
        self.stdInFile = str(testcase.std_in_file_name)
        self.commandExecutor = CommandExecutor()

    # Function to get resource limit for the testcase. During the creation of the testcase a Resource limit object with limits for various features
    # is also created (with default values if the instructor does not change this).
    # This function returns the dictionary mapping the attributes to their respective limits for this testcase.
    def get_resource_limit(self):
        try:
            resource = {}
            safeexec_obj = SafeExec.objects.get(testcase=self.testcase)
            attrs = ['cpu_time', 'clock_time', 'memory', 'stack_size', 'child_processes', 'open_files', 'file_size']
            for attr in attrs:
                val = getattr(safeexec_obj, attr)
                if val is not None:
                    resource[attr] = val
            return resource
        except SafeExec.DoesNotExist:
            return {}

    # Function to make a tarfile of all output files and return the name of this file.
    def make_tar(self):
        # Create the file containing std output with a certain pattern in its name. "standardOutput_testcase-id"
        stdoutFileName = "standardOutput_" + str(self.testcase.id)
        shutil.move(self.std_out, stdoutFileName)
        outputfiles = [stdoutFileName]

        # Set the name of the tarfile which is going to contain the output files.
        tarname = "output_file_" + str(self.testcase.id) + ".tar.bz2"
        outputFilesTar = tarfile.open(name=tarname, mode="w:bz2")

        # Add the std output file and all the other files that were created by the student solution (typically the files to which the student solution
        # wrote to other than the std output) to the tarfile.
        for afile in outputfiles + self.output_files:
            if os.path.isfile(afile):
                outputFilesTar.add(afile)
        outputFilesTar.close()
        return tarname

    # Function which is going to run the execution command on the input file of the testcase. Note that compilation if needed is done at the section
    # level itself.
    def run(self, exeCommand):
        # Create the output file to capture the std output in the current directory.
        _, self.std_out = tempfile.mkstemp()
        os.chmod(self.std_out, 0777)
        command = exeCommand

        # Add the command line arguments if any.
        if self.testcase.command_line_args:
            command = command + self.testcase.command_line_args

        # Then redirect the std input to the input file.
        if os.path.isfile(self.stdInFile):
            command = command + " < " + self.stdInFile

        # Execute the resulting command with the appropriate resource limits and the output file created above.
        self.testResults = self.commandExecutor.safe_execute(
                                                    command=command,
                                                    limits=self.get_resource_limit(),
                                                    outfile=self.std_out
                                                )

        # Check if the testcase has passed.
        self.passed = self.test_passed()

        # Incase the testcase has not passed the attrs dictionary below holds needed error messages and return code for the testcase.
        attrs = {'error_messages': "".join(self.testResults.stderr),
                 'return_code': int(self.testResults.returnCode),
                 'test_passed': self.passed}
        # This dictionary is used to filter out any existing testcase result for the submission so as to update it with the new results in attrs above.
        filter_attrs = {'test_case': self.testcase, 'program_result': self.program_result}

        # If any Testcase Results exist with the filter_attrs attributes, then update if with the new attributes.
        # Remove the older output file.
        # Else if none exist, then store the current result with the filter_attrs added to the attrs dictionary.
        try:
            obj = TestcaseResult.objects.filter(**filter_attrs)
            obj.update(**attrs)
            test_result = obj[0:1].get()
            default_storage.delete(test_result.output_files.path) # Remove older file.
        except TestcaseResult.DoesNotExist:
            attrs.update(filter_attrs)
            test_result = TestcaseResult.objects.create(**attrs)

        # Make a tar file of the std output file and the other files which have been written to by the student submission.
        # Update the test result (updated or newly created) with this tar file as the output file.
        tar_name = self.make_tar()
        test_result.output_files.save(tar_name, File(open(tar_name)))
        return self

    # Function to check if the student submission has passed the testcase.
    def test_passed(self):
        # Create a temporary directory and copy the expected output of the testcase to this file.
        temp_dir = tempfile.mkdtemp(prefix="grader_op_files")
        extract_or_copy(src=self.testcase.output_files.file.name, dest=temp_dir)
        std_output_file = str(self.testcase.std_out_file_name)

        # Other output files are stored in this variable.
        self.output_files = os.listdir(temp_dir)
        self.output_files.remove(std_output_file)

        # Now check for the status of the testcase. Call compare_output().
        is_passed = False
        print "Testcase return code is - ", self.testResults.returnCode
        if self.testResults.returnCode == 0: # Exited normally.
            is_passed = self.compare_output(temp_dir, std_output_file)

        # Remove the temporary directory and return the status of the testcase.
        shutil.rmtree(temp_dir, ignore_errors=True)
        return is_passed

    # Function to compare output of the standard output file and the actual output.
    # Takes as input the actual output file and expected output in that order.
    def compare_output(self, temp_dir, std_output_file):
        if not self.compare_file(os.path.join(temp_dir, std_output_file), self.std_out):
            return False

        for afile in self.output_files: # compare all O/P files.
            if not self.compare_file(afile, afile.split('/')[-1]):
                return False
        return True

    # Function to compare 2 files.
    # Takes as input the expected output and actual output file in that order.
    def compare_file(self, expectedop, actualop):
        # If the actual output is not valid return false.
        if not os.path.isfile(actualop):
            return False

        # Open both the files and see if they have the same length. If true proceed else return false.
        file1 = open(expectedop)
        file2 = open(actualop)

        if(len(list(file1)) > len(list(file2))):
            return False
        
        file1 = open(expectedop)
        file2 = open(actualop)
        
        # Compare the 2 files line by line.
        for line1, line2 in zip(file1, file2):
            if line1.strip() != line2.strip():
                return False

        for line2 in file2:
            if line2.strip() != "":
                return False
        return True

# Class to manage execution of student submissions at the section level.
# Stores as class members the assignment result, program model instance, files relevant to this section, language of the section, compilation and 
# execution command of the section, and a command executor to take care of compilation if necessary.
class Program(object):
    def __init__(self, program, assignment_result):
        self.assignment_result = assignment_result
        self.program = program

        # Extracting the list of files relevant to only this section.
        if program.program_files:
            prgrm_files = get_file_name_list(name=program.program_files.file.name)
            prgrm_files = " ".join(prgrm_files)
        else:
            prgrm_files = ""

        # Adding the list of files in the assignment model solution to the above list.
        self.programFiles = program.assignment.student_program_files + " " + prgrm_files
        self.language = program.assignment.program_language
        self.compiler_command = get_compilation_command(program)
        self.execution_command = get_execution_command(program)
        self.commandExecutor = CommandExecutor()

    # Function to check if any files are missing.
    def fileExist(self):
        self.missingFiles = []

        # Checking if each file in the self.programFiles variable is valid. If not add to the missing files array.
        for aFile in self.programFiles.split():
            if not os.path.isfile(aFile):
                self.missingFiles.append(aFile)

        # If there are any missing files, then either retrieve existing program result object or create one with the assignment result, section
        # and the missing files. If the object was not created, then update the missing files attribute of the program result.
        # Save the new or existing program result object after this, and return if there were any files missing.
        if self.missingFiles:
            self.programResult, created = ProgramResults.objects.get_or_create(
                                            assignment_result = self.assignment_result,
                                            program = self.program,
                                            defaults = {'missing_file_names': "\n".join(self.missingFiles)}
                                        )
            if not created:
                self.programResult.missing_file_names = "\n".join(self.missingFiles)

            self.programResult.save()
        return bool(self.missingFiles)
            
    # Function to handle compilation of the section.
    def compile(self):

        # If any files are missing then return failure of compilation. Appropriate program result is created.
        if self.fileExist():
            return False

        # If the language of the section/assignment needs compilation, then go ahead and compile. Set program result attributes accordingly.
        # If compilation is not needed then proceed.
        if compile_required(self.language):
            compilation_command = self.compiler_command
            self.compileResult = self.commandExecutor.executeCommand(command=compilation_command)
            attrs = {'missing_file_names': "\n".join(self.missingFiles),
                 'compiler_errors': "".join(self.compileResult.stderr),
                 'compiler_output': "\n".join(self.compileResult.get_stdout()),
                 'compiler_return_code': int(self.compileResult.returnCode)}
        else:
            attrs = {'missing_file_names': "\n".join(self.missingFiles),
                 'compiler_errors': "",
                 'compiler_output': "",
                 'compiler_return_code': 0}
        filter_attrs = {'assignment_result': self.assignment_result, 'program': self.program}

        # Create or update program result object with the result of compilation process for the section. The attributes of the program result object
        # are the same as the result of the compilation process.
        try: # create_or_update equivalent.
            obj = ProgramResults.objects.filter(**filter_attrs)
            obj.update(**attrs)
            self.programResult = obj[0:1].get()
        except ProgramResults.DoesNotExist:
            attrs.update(filter_attrs)
            self.programResult = ProgramResults.objects.create(**attrs)

        # If compilation is successful or if compilation is not needed then return true. Else return false.
        if compile_required(self.language) == False or self.compileResult.returnCode == 0:
            return True
        else:
            return False

    # Function to run the student solution on all the testcases of the section.
    def run(self):
        # Filter out the testcases of the section.
        testcases = Testcase.objects.filter(program=self.program)

        # Run the execution command on each of the testcases. Compilation (if needed) is already taken care of.
        for test in testcases:
            testcase = TestCase(test, self.programResult)
            testcase.run(self.execution_command)


# Class to manage evaluation of a submission. The submission id is passed during the creation of the Evaluate object.
# Class members are the submission, command executor and evaluation directory.
class Evaluate(object):
    def __init__(self, submission):
        self.commandExecutor = CommandExecutor()
        self.submission = submission
        self.eval_dir = os.path.join(PROJECT_ROOT, '../evaluate/safeexec')

    # Function to setup the evaluation directory.
    def setup(self, submission, program_type):
        # Create a temporary directory inside the evaluation directory. Copy the submission files into this directory.
        src = submission.filePath.file.name # gives absolute path
        self.temp_dir = tempfile.mkdtemp(prefix="grader", dir=self.eval_dir)
        os.chdir(self.temp_dir)
        extract_or_copy(src=src, dest=self.temp_dir)

        # Update or create the assignment result for the submission. Update the submitted files for existing assignment results.
        self.submittedFiles = get_file_name_list(name=src)
        self.assignment_result, _ = AssignmentResults.objects.get_or_create(
                                            submission=submission,
                                            defaults={'submitted_files': "\n".join(self.submittedFiles)}
                                        )
        self.assignment_result.is_stale = False
        self.assignment_result.save()

        # Assuming only 1 directory level, cd to that directory. If the student submitted only 1 file, then dont do anything.
        directories = [a for a in os.listdir('./') if os.path.isdir(a)]
        if directories:
            os.chdir(directories[0])
        currentDir = os.getcwd()

        # Copy the program files (of all sections) to this directory. Note that the solution file is still student's submission.
        programs = ProgramModel.objects.filter(assignment=submission.assignment)
        testcaseList = []
        for program in programs:
            testcaseList.append(Testcase.objects.filter(program=program))
            if program.program_files:
                extract_or_copy(src=program.program_files.file.name, dest=currentDir)

        # Copy input-output files for all testcases. Now we are ready for the evaluation process.
        for testcase in testcaseList:
            for test in testcase:
                if test.input_files:
                    extract_or_copy(src=test.input_files.file.name, dest=currentDir)

    # Function to clean up the directories setup for the evaluation process.
    def cleanUp(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    # Function called to retrieve the results of the student submission once the Evaluate object is created.
    def getResults(self, program_type="Evaluate"):
        # Setup the directories for the evaluation process.
        self.setup(self.submission, program_type)

        # Collect the section for the assignment.
        allPrograms = ProgramModel.objects.filter(assignment=self.submission.assignment, program_type=program_type)

        # For each section, compile the section if needed and if compilation is successful then execute the solution on all testcases of the section.
        for program in allPrograms:
            prgrmObject = Program(program, self.assignment_result)
            if prgrmObject.compile():
                prgrmObject.run()

        # Clean up the temp directories and return the results.
        self.cleanUp()
        return Results(self.submission, program_type=program_type)

    # Same as the above though frankly I dont know why this is here!! :O
    def eval(self, program_type):
        self.setup(self.submission, program_type)
        allPrograms = ProgramModel.objects.filter(assignment=self.submission.assignment, program_type=program_type)
        for program in allPrograms:
            prgrmObject = Program(program, self.assignment_result)
            if prgrmObject.compile():
                prgrmObject.run()
        self.cleanUp()

# Class to manage the results of a student submission. This is used to transfer data from the server to the client. This has nothing to do with the
# storing the results to the database.
class Results(object):
    def __init__(self, submission, program_type):
        self.assignment_result = AssignmentResults.objects.get(submission=submission)
        program_objects = ProgramResults.objects.filter(assignment_result=self.assignment_result)
        
        self.program_results = []

        for aProgramResult in program_objects:
            if aProgramResult.program.program_type == program_type:
                self.program_results.append(self.ProgramResultSaved(aProgramResult, program_type))

        self.marks = reduce(lambda x,y: x + y.marks, self.program_results, 0)

    class ProgramResultSaved(object):
        def __init__(self, program_result, program_type):
            self.program_result = program_result # Used in template.
            self.compiler_command = get_compilation_command(program_result.program)
            self.execution_command = get_execution_command(program_result.program)
            all_obj = TestcaseResult.objects.filter(program_result=program_result)
            test_type_obj = [a for a in all_obj]
            self.testResults = [Results.TestcaseResultSaved(obj) for obj in test_type_obj]

            self.marks = reduce(lambda x,y: x + y.marks, self.testResults, 0)

    class TestcaseResultSaved(object):
        def __init__(self, test_case_result):
            self.test_case = test_case_result.test_case
            self.program_result = test_case_result.program_result
            self.error_messages = test_case_result.error_messages
            self.return_code = test_case_result.return_code
            self.test_passed = test_case_result.test_passed
            self.output_files = test_case_result.output_files

            std_output_file_name = "standardOutput_" + str(self.test_case.id)
            tar = tarfile.open(self.output_files.file.name)
            self.actual_output = tar.extractfile(std_output_file_name).readlines()
            self.expected_output = read_file(self.test_case.std_out_file_name, name=self.test_case.output_files.file.name)
            self.marks = (self.test_case.marks or 0) if self.test_passed else 0
