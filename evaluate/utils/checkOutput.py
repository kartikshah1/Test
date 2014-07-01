from evaluate.utils.executor import CommandExecutor
from utils.archives import get_file_name_list, extract_or_copy
from grader.settings import PROJECT_ROOT

import pickle, os, shutil, tempfile

# Class to manage custom testcases (student fed input files)
class CustomTestcase(object):
    def __init__(self, inputFile, program, submission):
        # Setting section of the testcase, submission to use, the input file given by the student and the command executor that runs the commands.
        self.program = program
        self.submission = submission
        self.inputFile = inputFile
        self.commandExecutor = CommandExecutor()
        self.eval_dir = os.path.join(PROJECT_ROOT, '../evaluate/safeexec')

    def get_resource_limit(self):
        # Return default values because there is no setting for custom testcase.
        return {'cpu_time':10, 'clock_time':10,
                'memory': 32768, 'stack_size': 8192, 'child_processes': 0,
                'open_files': 512, 'file_size': 1024,
            }

    # Store the input file that student uploaded  
    def store_input_file(self, inputFile, dest):
        file_path = os.path.join(dest, inputFile.name.split('/')[-1])
        destination = open(file_path, 'wb+')

        # Work-around to support file and InMemoeryUploadedFile objects
        if hasattr(inputFile, 'chunks'):
            all_file = inputFile.chunks()
        else:
            all_file = inputFile

        # Write everything to the input file represented by destination object. Then return the full path of file name.
        for chunk in all_file:
            destination.write(chunk)
        destination.close()
        return file_path

    # Function to setup the environment (input file, solution files and submission files) before running the code.
    def setup(self):
        # This is the directory where the student program is copied to.
        self.temp_dir = tempfile.mkdtemp(prefix="grader", dir=self.eval_dir)
        os.chdir(self.temp_dir)

        # Copy student solution files to tmp directory.
        extract_or_copy(src=self.submission.filePath.file.name, dest=self.temp_dir)

        # Another temp directory for running solution program. This is the directory where the solution program is copied to.
        self.solution_temp_dir = tempfile.mkdtemp(prefix="solution", dir=self.eval_dir)
        
        directories = [a for a in os.listdir('./') if os.path.isdir(a)]
        if directories:
            os.chdir(directories[0])
        currentDir = os.getcwd()

        # Extract the program file and the input file to the student directory, and the input file to the program directory as well.
        extract_or_copy(src=self.program.program_files.file.name, dest=currentDir)
        self.submittedFiles = get_file_name_list(name=self.submission.filePath.file.name)
        input_file = self.store_input_file(self.inputFile, currentDir)
        shutil.copy(src=input_file, dst=self.solution_temp_dir)

    # Function to compile the student program.
    def compile(self):
        self.exe_file = str(self.program.id)
        compiler_command = " ".join(pickle.loads(self.program.compiler_command)) + " -o " + self.exe_file
        self.compileResult = self.commandExecutor.executeCommand(command=compiler_command)

    # Function to run the student and model solution on the input file.
    def run(self):
        # Run student exe file.
        _, self.actual_stdout = tempfile.mkstemp(dir='./')
        os.chmod(self.actual_stdout, 0777)

        runStudentProgram = "./" + self.exe_file + " < " + self.inputFile.name
        self.actualOutput = self.commandExecutor.safe_execute(
                                                        command=runStudentProgram,
                                                        limits=self.get_resource_limit()
                                                    )

        # Run solution exe file.
        shutil.copy(src=self.program.exe_file_name.file.name, dst=self.solution_temp_dir)
        os.chdir(self.solution_temp_dir)
        _, self.expected_stdout = tempfile.mkstemp(dir='./')
        os.chmod(self.expected_stdout, 0777)
        exe = self.program.exe_file_name.name.split('/')[-1]
        runSolutionProgram = "./" + exe + " < " + self.inputFile.name

        self.expectedOutput = self.commandExecutor.safe_execute(
                                                        command=runSolutionProgram,
                                                        limits=self.get_resource_limit()
                                                    )
        self.passed = self.testPassed()

    # This function is called after run(), and checks the actual and the expected output.
    def testPassed(self):
        # At this point actual o/p is in self.actual_stdout and expected O/P is in self.expected_stdout.
        # compare them and display result on browser.

        if not (self.expectedOutput.returnCode == 0 and self.actualOutput.returnCode == 0):
            return False

        exp_op = iter(self.expectedOutput.get_stdout())
        act_op = iter(self.actualOutput.get_stdout())

        if len(self.expectedOutput.get_stdout()) > len(self.actualOutput.get_stdout()):
            return False

        for line1, line2 in zip(exp_op, act_op):
            if line1.strip() != line2.strip():
                return False
    
        for line2 in act_op:
            if line2.strip() != "":
                return False
        return True

    # This is the function called to get the result once the input file is uploaded.
    def getResult(self):
        # Setup the environment.
        self.setup()
        # Compile the program.
        self.compile()
        # If compilation is successful then run the program.
        if self.compileResult.returnCode == 0:
            self.run()
        # Clean up the temporary directories.
        self.cleanUp()
        return self

    # Function to clean up the temporary directories.
    def cleanUp(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
