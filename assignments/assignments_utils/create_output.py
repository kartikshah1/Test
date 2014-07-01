from evaluate.utils.executor import CommandExecutor
from utils.archives import get_file_name_list, extract_or_copy
from grader.settings import PROJECT_ROOT
from utils.filetypes import is_intermediate_files, compile_required, get_execution_command, get_compilation_command
#from assignments.models import SafeExec

import os, shutil, tempfile, tarfile


# Creates output for different testcase instances
class CreateOutput(object):
    def __init__(self, instance):
        self.program = instance.program
        self.testcase = instance
        self.input_files = instance.input_files
        self.commandExecutor = CommandExecutor()
        self.failed = False
        self.eval_dir = os.path.join(PROJECT_ROOT, '../evaluate/safeexec')

    # Function to get resource limit for the testcase. During the creation of the testcase a Resource limit object with limits for various features
    # is also created (with default values if the instructor does not change this).
    # This function returns the dictionary mapping the attributes to their respective limits for this testcase.
    def get_resource_limit(self):
        return {'cpu_time':10, 'clock_time':10,
                    'memory': 32768, 'stack_size': 8192, 'child_processes': 0,
                    'open_files': 512, 'file_size': 1024,
                    }
                    
        '''
        Solve this by actually retrieving the exact SafeExec object.
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
            return {'cpu_time':10, 'clock_time':10,
                    'memory': 32768, 'stack_size': 8192, 'child_processes': 0,
                    'open_files': 512, 'file_size': 1024,
                    }
        '''


    # Setup the output creator
    def setup(self):
        # create temporary directory.
        self.temp_dir = tempfile.mkdtemp(prefix="solution", dir=self.eval_dir)
        os.chdir(self.temp_dir)

        currentDir = os.getcwd()

        # Copy program files and input files to the directory
        if self.program.program_files :
            extract_or_copy(src=self.program.program_files.file.name, dest=currentDir)
        if self.program.assignment.model_solution:
            extract_or_copy(src=self.program.assignment.model_solution.file.name, dest=currentDir)

        # write input file to temporary file.
        self.temp_input_d = tempfile.mkdtemp(prefix="input")
        if self.input_files:
            self.input = os.path.join(
                                self.temp_input_d,
                                os.path.basename(self.testcase.input_files.file.name)
                            )
            f = open(self.input, 'w')
            for a_line in self.input_files.file:
                f.write(a_line)
            f.close()
            # input file has been written now extract.
            extract_or_copy(src=self.input, dest=currentDir)
        else:
            self.input = ''

    # Run the program solution files and 
    def run(self):
        # Compile the solution. If there are errors then write it to the error file and return
        if compile_required(self.program.language):
            compiler_command = get_compilation_command(self.program)
            print "Compiling model solution. Compilation Command - " + compiler_command
            self.command_output = self.commandExecutor.safe_execute(
                                                            command=compiler_command,
                                                            limits=self.get_resource_limit()
                                                        )
            if self.command_output.getReturnCode():
                # There was some error. Write it in database.
                print "Compilation of model solution failed."
                self.failed = True
                _, self.error_file = tempfile.mkstemp(prefix="error", dir=self.temp_input_d)
                f = open(self.error_file, 'w')

                for a_line in self.command_output.get_stderr():
                    f.write(a_line)
                f.close()
                return

        # No errors and thus can continue. Run the solution
        execution_command = get_execution_command(self.program)
        print "Creating Output. Running following execution command - " + execution_command
        #if self.testcase.command_line_args:
        #    execution_command = execution_command + self.testcase.command_line_args
        if self.testcase.std_in_file_name:
            execution_command = execution_command + " < " + self.testcase.std_in_file_name
        self.command_output = self.commandExecutor.safe_execute(
                                                            command=execution_command,
                                                            limits=self.get_resource_limit()
                                                        )
        self.success = bool(self.command_output.getReturnCode())
        self.command_output.printResult()

        # Delete input files from current directory. And the program files
        dir_content = os.listdir('./')
        for a_file in dir_content:
            if self.is_program_file(a_file):
                os.remove(a_file)

        if self.input:
            for a_file in get_file_name_list(name=self.input): # delete extracted files
                if os.path.isfile(a_file):
                    os.remove(a_file)

        # Write standard output to a file and save it in database.
        directory_content = os.listdir('./')

        _, self.std_out_file = tempfile.mkstemp(prefix='output', dir="./")
        out_file = open(self.std_out_file, 'w')

        for a_line in ["\n".join(self.command_output.get_stdout())]:
            out_file.write(a_line)
        out_file.close()

        # There was some error. Write it in database.
        if self.command_output.getReturnCode():
            self.failed = True
            _, self.error_file = tempfile.mkstemp(prefix="error", dir=self.temp_input_d)
            f = open(self.error_file, 'w')

            for a_line in self.command_output.get_stderr():
                f.write(a_line)
            f.close()

        # If directory has any content left then make a tar, else set the outfile to the output file.
        if directory_content: # make a tar
            self.out_file = self.make_tar(directory_content + [self.std_out_file], self.std_out_file)
        else: # there are no other files standard output only.
            self.out_file = self.std_out_file

    def get_stdout_file_name(self):
        return os.path.basename(self.std_out_file)

    def get_stderr_file_name(self):
        return os.path.basename(self.error_file)

    def get_stderr_file_path(self):
        return self.error_file

    def make_tar(self, files, tarname):
        tarname = tarname + ".tar.bz2"
        output_files_tar = tarfile.open(name=tarname, mode="w:bz2")

        # Make tar file from all output files.
        for afile in files:
            if os.path.isfile(afile):
                output_files_tar.add(os.path.basename(afile))
        output_files_tar.close()
        return tarname


    def get_output(self):
        prev_dir = os.getcwd()
        try:
            self.setup()
            self.run()
        finally:
            os.chdir(prev_dir)

        return self

    def is_program_file(self, fname):
        filename = fname.split("/")[-1]
        if self.program.program_files and filename in get_file_name_list(self.program.program_files.file.name):
            return True
        elif self.program.assignment.model_solution and filename in get_file_name_list(self.program.assignment.model_solution.file.name):
            return True
        elif is_intermediate_files(filename,self.program,self.program.language):
            return True
        else:
            return False

    def clean_up(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
        shutil.rmtree(self.temp_input_d, ignore_errors=True)