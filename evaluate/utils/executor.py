from grader.settings import PROJECT_ROOT

import subprocess
import threading, os, psutil

# Class to manage command execution.
class CommandExecutor(object):
    def __init__(self):
        self.process = None
        self.result = None
        self.sandbox = os.path.join(PROJECT_ROOT, 'safeexec')

    # Function to run the command using the process interface of python.
    # Takes as input the command to be run, and the output file to write the standard output to.
    def run(self, command, outfile):
        # Setup command line.
        commandLine = ["/bin/bash", "-c", command]

        # Setup output file if it has been passed as an argument. If the output file is valid then open the file as a file object.
        # Else capture the std output separately.
        if outfile and os.path.isfile(outfile):
            outfile_obj = open(outfile, 'wb')
        else:
            outfile_obj = None

        # Open a subprocess with the command line, output file object. Wait for the process to finish.
        self.process = subprocess.Popen(
                            commandLine,
                            stdout=outfile_obj or subprocess.PIPE,
                            stderr=subprocess.PIPE
                        )
        self.process.wait()

        # Collect the std error and return code of the process.
        cmdError = self.process.stderr.readlines()
        returnCode = self.process.returncode

        # If output file object has been created then close it and set the stdoutfile variable to outfile. This will be used to create CommandResult.
        # Else collect command line output in cmd_output and set stdoutfile to none.
        if outfile_obj:
            outfile_obj.close()
            stdoutfile = outfile
            cmd_output = None
        else:
            cmd_output = [aLine.strip() for aLine in self.process.stdout.readlines()]
            stdoutfile = None

        # Set self.result to CommandResult with the command, command line output, std error, return code, and the stdoutfile as arguments.
        self.result = CommandResult(command, cmd_output, cmdError, returnCode, stdoutfile)

    # Function to execute command. Calls the run function.
    def executeCommand(self, command, outfile=None):
        # Call run function with the right arguments.
        self.run(command, outfile=outfile)
        # Return the self.result object, which is set in run() function.
        return self.result

    # Function to execute command using safe-exec environment. It uses the limits passed as arguments.
    # Takes as input command, limits and the outfile for the output to be written to.
    def safe_execute(self, command, limits, outfile=None):
        # For now use run() directly.
        self.run(command, outfile)
        return self.result
        '''
        Solve the safeexec bug. Once the bug is solved, remove the above 2 lines and uncomment this part.
        # Arguments dictionary for the safe-exec features. Maps the features to the command line options for the safe-exec executable.
        # Construct the run time parameters using the limit dictionary.
        args = {'cpu_time': '--cpu', 'clock_time': '--clock',
                'memory': '--mem', 'stack_size': '--stack',
                'child_processes': '--nproc', 'open_files': '--nfile',
                'file_size': '--fsize', 'env_vars': '--env_vars'}
        run_params = ' '
        for a in limits.keys():
            run_params = run_params + args[a] + ' ' + str(limits[a]) + ' '

        # Construct new command with the actual command passed to the safe-exec executable with the limits parameters.
        # Call run() function with the new command.
        command = self.sandbox + run_params + ' --exec ' + command
        self.run(command, outfile)
        return self.result
        '''

# Class to manage the results of a command run by the CommandExecutor.
# Takes as input the command, std output, std error, return code and the output file of the command execution.
class CommandResult(object):
    def __init__(self, command, stdout, stderr, returnCode, outfile=None):
        self.command = command
        self.outfile = outfile
        self.stdout = stdout
        self.stderr = stderr
        self.returnCode = returnCode

    # Function to return the command.
    def get_command(self):
        return self.command

    # Function to return the standard output.
    # Extracts the standard output from either the outfile or the stdout variables.
    def get_stdout(self):
        # If self.outfile exists then extract the output from this file.
        # Else return the self.stdout variable.
        if self.outfile:
            if os.path.isfile(self.outfile):
                with open(self.outfile, 'r') as f:
                    return [line for line in f]
            else:
                raise Exception("output was written to a file. That file was not found.")
        else:
            return self.stdout

    # Function to return the standard error.
    def get_stderr(self):
        return self.stderr

    # Function to return the return code of the command execution.
    def getReturnCode(self):
        return self.returnCode

    # Function to print the attributes for logging.
    def printResult(self):
        print "Command Executed - ",self.command
        print "Return Code - ",self.returnCode
        print "Standard error if any - ",self.stderr