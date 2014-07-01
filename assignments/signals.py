'''
This file is not being used currently.
'''

from grader.settings import MEDIA_ROOT
from evaluate.utils.executor import CommandExecutor
import os, tarfile, shutil

rootPath = os.path.realpath(os.path.dirname(__file__))
tmpDir = os.path.join(rootPath, "tmp")

# Compile model solution
def compile_model_solution(sender, instance, **kwargs):
    # If source file was not changed no need to re-compile.
    if not hasattr(instance, 'source_changed'): 
        return

    if not kwargs.get('created'):
        print "Not created!"

    programFilePath = instance.program_files.name
    ModelSolutionPath = instance.model_solution.name
    
    # Model Solution was not provided hence do nothing.
    if os.path.isdir(ModelSolutionPath):
        return

    os.chdir(tmpDir)

    extractFile(os.path.join(MEDIA_ROOT, ModelSolutionPath), tmpDir)

    # Change directory if solution tar contains a directory.
    if os.path.isdir(os.listdir('./')[0]):
        os.chdir(os.listdir('./')[0])

    currentDir = os.getcwd()
    extractFile(os.path.join(MEDIA_ROOT, programFilePath), currentDir)

    # Setting up compilation and creating CommandExecutor
    executor = CommandExecutor(timeout=5)
    command = get_compilation_command(instance)
    ''' To Remove: COMPILER_FLAGS
    exeName = "exefile_" + str(instance.id)
    compilerFlags = instance.compiler_flags if instance.compiler_flags else ""
    command = instance.compiler_name + " " + compilerFlags\
                + " " + instance.file_names_to_compile + " " + " -o " + exeName
    '''
    compileResult = executor.executeCommand(command=command)

    # Update output files on success
    if compileResult.returnCode == 0: 
        instance.UpdateOutput()
    cleanUp()


# Delete all content of testDir.
def cleanUp():
    os.chdir(tmpDir)
    for item in os.listdir(os.getcwd()):
        if os.path.isfile(item): os.remove(item)
        if os.path.isdir(item): shutil.rmtree(item)

# Extracts the compressed file.
def extractFile(src, dest):
        tar = tarfile.open(src)
        tar.extractall(path=dest)
        tar.close()
