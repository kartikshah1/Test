'''
Created on Jun 3, 2013
@author: aryaveer
'''

from grader.settings import MEDIA_ROOT
from evaluate.utils.executor import CommandExecutor
from assignments_utils.create_output import CreateOutput
from django.core.files import File

import os, shutil, pickle, tempfile
from utils.archives import Archive
from utils.filetypes import get_compiler_name, get_compilation_command, compile_required
from django.db import models

rootPath = os.path.realpath(os.path.dirname(__file__))
tmpDir = os.path.join(rootPath, "tmp")

# pre_delete receiver common for all models.
def delete_files(sender, instance, **kwargs):
    for field in instance._meta.fields: 
        if isinstance(field, models.FileField):
            filefield = getattr(instance, field.name)
            if filefield:
                filefield.delete(save=False)

# This receiver checks if the program solution is fine by compilation standards.
# post_save receiver.
def compile_solution(sender, instance, **kwargs):

    # If the program language is an interpreted language, then we dont do anything
    if not compile_required(instance.assignment.program_language) and not getattr(instance, 'execute_now', False):
        instance.set_sane()
        instance.delete_error_message()
        return

    if not compile_required(instance.assignment.program_language) :
        old_pwd = os.getcwd()
        instance.set_sane()
        instance.UpdateOutput()
        instance.delete_error_message()
        os.chdir(old_pwd)
        return

    # instance.id would indicate that record was not created.
    if not getattr(instance, 'compile_now', False) or instance.id is None: 
        return

    # If solution is given then set the path, else do nothing
    programFilePath = instance.program_files.name
    if hasattr(instance.assignment.model_solution, 'file'):
        ModelSolutionPath = instance.assignment.model_solution.file.name
    else:
        instance.set_sane()
        instance.delete_error_message()
        return 

    # Model Solution was not provided hence do nothing.
    if not os.path.isfile(ModelSolutionPath):
        return

    # Copying module solution to a temp directory for compilation
    tmp_dir = tempfile.mkdtemp(prefix='grader')
    old_pwd = os.getcwd()
    os.chdir(tmp_dir)
    currentDir = os.getcwd()
    try:
        # Copy model solution to temp directory.
        with Archive(fileobj=instance.assignment.model_solution.file) as archive:
            if archive.is_archive():
                archive.extract(dest=currentDir)
            else:
                shutil.copy(src=os.path.join(MEDIA_ROOT, ModelSolutionPath), dst=currentDir)

        # Change directory if solution tar contains a directory.
        directories = [a for a in os.listdir('./') if os.path.isdir(a)]
        if directories:
            os.chdir(directories[0])
            currentDir = os.getcwd()

        # Copying the program files to the current directory
        if instance.program_files:
            with Archive(name=instance.program_files.file.name) as archive:
                if archive.is_archive():
                    archive.extract(dest=currentDir)
                else:
                    shutil.copy(src=os.path.join(MEDIA_ROOT, programFilePath), dst=currentDir)

        # Setting up compilation process and calling the CommandExecutor with appropriate command
        executor = CommandExecutor(timeout=100)
        compiler_command = get_compilation_command(instance)
        compileResult = executor.executeCommand(command=compiler_command)

        # Compilation successful => Set the program to sane and delete errors, else report the errors.
        if compileResult.returnCode == 0: # save exe file on success.
            instance.is_sane = True
            instance.UpdateOutput()
            instance.delete_error_message()
        else:
            message = "Compilation failed.\nReturn code = {0}.\nError message={1}".format(compileResult.returnCode, "".join(compileResult.stderr))
            print "Instructor solution not sane - " + message
            instance.save_error(message)
        shutil.rmtree(tmp_dir)
    finally:
        os.chdir(old_pwd)


# It is a post_save handler of Assignment model. This verifies all the programs of the assignment
def verify_all_programs(sender, instance, **kwargs):
    if not getattr(instance, 'verify_programs', False):
        return # nothing to do

    all_programs = instance.program_model.objects.filter(assignment=instance)
    msg = ""
    for aprogram in all_programs:
        # If assignment program language is changed then check if the program language is correct, else point the errors.
        if 'program_language' in instance.changed_list:
            if aprogram.language != instance.program_language:
                aprogram.save_error("Programming language was changed in assignment. Please update this program accordingly.")
                continue
            else:
                aprogram.is_sane = True
                aprogram.save()
                aprogram.delete_error_message()
        # If the program files have been changed then, files in compiler command should either be in student program files 
        # or in additional files of program.
        if 'student_program_files' in instance.changed_list:
            file_list = []
            if aprogram.program_files:
                with Archive(fileobj=aprogram.program_files.file) as archive:
                    if archive.is_archive():
                        file_list = [a.split("/")[-1] for a in archive.getfile_members()]
                    else:
                        file_list = [aprogram.program_files.name.split("/")[-1]]

            file_list.extend(instance.student_program_files.split())
            file_to_compile = get_compilation_command_files(aprogram)
            file_to_execute = get_execution_command_files(aprogram)
            missing_file = set(file_to_compile) + set(file_to_execute) - set(file_list)

            # Some files are missing
            if missing_file:
                msg = "Files {0} are missing form this program please upload these files.".format(" ".join(missing_file))
                aprogram.save_error(msg)
                continue
            else:
                aprogram.is_sane = True
                aprogram.save()
                aprogram.delete_error_message()

        # If you reach here, everything is good. Now compile.
        if 'model_solution' in instance.changed_list:
            aprogram.compile_now = True
            aprogram.execute_now = True
            aprogram.save()

# Delete all content of testDir.
def cleanUp():
    os.chdir(tmpDir)
    for item in os.listdir(os.getcwd()):
        if os.path.isfile(item): os.remove(item)
        if os.path.isdir(item): shutil.rmtree(item)


# This creates the output of testcases if they are not provided. pre_save handler of Testcase model
def create_op_files(sender, instance, **kwargs):
    # If output files are provided do save them as it.
    if instance.output_files:
        pass
    # If they are not, then generate output file.
    else:
        instance.gen_op_obj = CreateOutput(instance).get_output()
        instance.output_files = File(
                                     open(instance.gen_op_obj.out_file),
                                     name=os.path.basename(instance.gen_op_obj.out_file)
                                )
        instance.std_out_file_name = instance.gen_op_obj.get_stdout_file_name()


# post_save handler of Testcase model. This method effectively cleans temporary files created during automatic generation of output files.
def testcase_cleanup(sender, instance, **kwargs):
    if hasattr(instance, 'gen_op_obj'):
        # If object is saved and program has some error.
        if instance.gen_op_obj.failed and hasattr(instance, 'id'):
            instance.solution_ready = False
            print "Saving error file"
            instance.save_error(error_file=instance.gen_op_obj.get_stderr_file_path())
        elif not instance.gen_op_obj.failed:
            instance.solution_ready = True
            instance.program.solution_ready = bool(instance.program.solution_ready and instance.solution_ready)
            instance.clear_error()
            print "Clear and set solution_ready to true!"
        else:
            instance.clear_error()
            print "Clear and set solution_ready to true (last else)!"
        instance.gen_op_obj.clean_up()
    # output file was given.
    else: 
        instance.clear_error()
        print "Clear and set solution_ready to true (outer else)!"