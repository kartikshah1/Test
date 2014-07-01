'''
Created on May 20, 2013
@author: aryaveer
'''
from django import forms
import pickle
from django.forms.util import ErrorList
from django.utils import timezone
from django.forms import widgets

from utils.archives import Archive
from utils.filetypes import is_valid, VALID_EXTENSIONS_COMPILERS, VALID_EXTENSIONS_INTERPRETERS, LANGUAGES, get_extension, get_compiler_name, get_interpreter_name, compile_required, execution_command_required
from assignments.models import Assignment

class DivErrorList(ErrorList):
    def __unicode__(self):
        return self.as_divs()
    def as_divs(self):
        if not self: return u''
        return u'<div class="alert alert-error">%s</div>' % ''.join([u'<div class="error">%s</div>' % e for e in self])

# IMPORTANT: make sure all form fields are exactly the same as corresponding model fields.
# TODO: May be try writing a method to do the above check.
class AssignmentForm(forms.Form):
    name = forms.CharField(label="Assignment Name")
    deadline = forms.DateTimeField(
                    input_formats=['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d', '%Y/%m/%d %H:%M'],
                    label="Soft Deadline",
                    help_text="Students can submit after this date if late submission is allowed."
                )
    hard_deadline = forms.DateTimeField(
                    input_formats=['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d', '%Y/%m/%d %H:%M'],
                    label="Hard Deadline",
                    help_text="Students can not submit after this date, if late submission is allowed."
                )
    late_submission_allowed = forms.BooleanField(
                                required=False,
                                label="Late Submission Allowed?",
                                help_text="If checked, students will be able to submit until hard deadline",
                            )
    choices = [(a, a) for a in LANGUAGES]
    program_language = forms.ChoiceField(
                        choices=choices,
                        label="Choose programming language",
                    )
    student_program_files = forms.CharField(
                            label="List of files name that student must submit",
                            help_text="File names separated by space.\
                                    (File name shouldn't have space.)"
                        )
    document = forms.FileField(
                    required=False,
                    label="Documents",
                    help_text="e.g. Some tutorial."
                    )
    helper_code = forms.FileField(
                    required=False,
                    label="Helper Code",
                    help_text="Provide students with code template or libraries."
                )
    model_solution = forms.FileField(
                        error_messages={'invalid': 'File was not a valid tar file.'},
                        required=False,
                        label="Solution Code(if any)",
                        help_text="Accepted archives are tar, tar.gz, tar.bz2, zip."
                    )
    publish_on = forms.DateTimeField(
                    label="Publish this assignment on",
                    input_formats=['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d', '%Y/%m/%d %H:%M']
                )
    description = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        kwargs['error_class']=DivErrorList
        super(AssignmentForm, self).__init__(*args, **kwargs)

    def clean_name(self):
        if not hasattr(self, 'this_course'):
            return self.cleaned_data['name']
        try:
            _ = Assignment.objects.get(name=self.cleaned_data['name'], course=self.this_course)
            raise forms.ValidationError('This assignment already exists in this course.')
        except Assignment.DoesNotExist:
            pass
        return self.cleaned_data['name']

    def clean_deadline(self):
        deadline = self.cleaned_data['deadline']
        if deadline and deadline < timezone.now():
            raise forms.ValidationError('Deadline can not be in past.')
        return self.cleaned_data['deadline']

    def check_model_solution(self, data):
        self._solution_file = []
        if 'model_solution' in self.changed_data:
            if data.get('model_solution', ""):
                with Archive(fileobj=data['model_solution']) as archive:
                    if not archive.is_archive():
                        if not is_valid(filename=data['model_solution'].name, lang=data['program_language']):
                            self._errors['model_solution'] = self.error_class(["This file was not valid."])
                            del data['model_solution']
                        else:
                            self._solution_file = [data['model_solution'].name]
                    else:
                        self._solution_file = [a.split("/")[-1] for a in archive.getfile_members()]
            else: # File is being deleted.
                pass
        else: # No change in file field. Check if file exist in database.
            if not hasattr(self, 'assignment_model'):
                return # Assignment is created without model solution.

            if not self.assignment_model.model_solution: return # no file in database.

            with Archive(fileobj=self.assignment_model.model_solution.file) as archive:
                if archive.is_archive():
                    self._solution_file = [a.split("/")[-1] for a in archive.getfile_members()]
                else:
                    file_name = self.assignment_model.model_solution.name.split("/")[-1]
                    self._solution_file = [file_name]

    def check_student_program_files(self, data):
        file_list = data.get('student_program_files').split()
        language = data.get('program_language')
        for afile in file_list:
            if not is_valid(afile, language):
                self._errors['student_program_files'] = self.error_class(["Only {1} files are accepted for {0} language.\
                    ".format(language, " ".join(get_extension(language)))])
                del data['student_program_files']
                break

    def clean(self):
        cleaned_data = super(AssignmentForm, self).clean()
        if self.errors: return cleaned_data

        self.check_student_program_files(cleaned_data)
        if self.errors: return cleaned_data

        self.check_model_solution(cleaned_data)
        if self._errors: return cleaned_data

        # file name to be compiled -- program files submitted by student should be in Teacher supplied tar.
        students_file_name = cleaned_data.get('student_program_files', "")
        students_file = set(students_file_name.split())
        missing_file = students_file  - set(self._solution_file)

        if missing_file and self._solution_file:
            self._errors['model_solution'] = self.error_class(["{0} was not found. Please upload {1}".format(" ".join(missing_file), students_file_name)])
            del cleaned_data['model_solution']

        if cleaned_data.get('deadline') > cleaned_data.get('hard_deadline'):
            self._errors['hard_deadline'] = self.error_class(['Hard deadline should be later than soft deadline'])

        return cleaned_data

class CompilerCommandWidget(widgets.MultiWidget):
    def __init__(self, *args, **kwargs):
        widgets = [forms.TextInput(attrs={'readonly':'True'}),
                   forms.TextInput,
                   forms.TextInput]
        super(CompilerCommandWidget, self).__init__(widgets, *args, **kwargs)

    def decompress(self, value):
        if value:
            return pickle.loads(value)
        else:
            return ['', '', '',]

class CompilerCommand(forms.fields.MultiValueField):
    widget = CompilerCommandWidget

    def __init__(self, *args, **kwargs):
        list_fields = [forms.fields.CharField(max_length=512, widget=forms.TextInput(attrs={'readonly':'True'}), required=False),
                       forms.fields.CharField(max_length=512, required=False),
                       forms.fields.CharField(max_length=512)]
        super(CompilerCommand, self).__init__(list_fields, *args, **kwargs)

        self.widget = CompilerCommandWidget()

    def compress(self, values):
        if values:
            if values[0] in forms.fields.EMPTY_VALUES:
                raise forms.fields.ValidationError("Please provide compiler name")
            if values[2] in forms.fields.EMPTY_VALUES:
                raise forms.fields.ValidationError("Please provide file names.")
        return pickle.dumps(values)


class ExecutionCommandWidget(widgets.MultiWidget):
    def __init__(self, *args, **kwargs):
        widgets = [forms.TextInput(attrs={'readonly':'True'}),
                   forms.TextInput,
                   forms.TextInput]
        super(ExecutionCommandWidget, self).__init__(widgets, *args, **kwargs)

    def decompress(self, value):
        if value:
            return pickle.loads(value)
        else:
            return ['', '', '',]

class ExecutionCommand(forms.fields.MultiValueField):
    widget = ExecutionCommandWidget

    def __init__(self, *args, **kwargs):
        list_fields = [forms.fields.CharField(max_length=512, widget=forms.TextInput(attrs={'readonly':'True'}), required=False),
                       forms.fields.CharField(max_length=512, required=False),
                       forms.fields.CharField(max_length=512)]
        super(ExecutionCommand, self).__init__(list_fields, *args, **kwargs)

        self.widget = ExecutionCommandWidget()

    def compress(self, values):
        if values:
            if values[0] in forms.fields.EMPTY_VALUES:
                raise forms.fields.ValidationError("Please provide name of the interpreter")
            if values[2] in forms.fields.EMPTY_VALUES:
                raise forms.fields.ValidationError("Please provide file names.")
        return pickle.dumps(values)


class ProgramFormCNotE(forms.Form):
    #error_css_class = 'alert-error'
    #required_css_class = 'alert-error'
    PROGRAM_TYPES = (
                      ('Evaluate', 'Evaluate'),
                      ('Practice', 'Practice'),
                    )
    name = forms.CharField()
    program_type = forms.ChoiceField(choices=PROGRAM_TYPES)
    compiler_command = CompilerCommand(
                            help_text="Give compiler flags in second field and file names in third field. File names can be any of the files from student submission provided in assignment details.\
                            If you provide other file names, upload those files in additional files below.",
                            required=False
                        )
    program_files = forms.FileField(
                        error_messages={'invalid': 'File was not a valid tar file.',},
                        required = False,
                        label="Additional Source Files",
                        help_text="Provide additional source files here.\
                                Accepted archives are tar, tar.gz, tar.bz2, zip."
                    )
    makefile = forms.FileField(
                    required=False,
                    help_text="Must be a text file."
                )
    description = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        kwargs['error_class']=DivErrorList
        super(ProgramFormCNotE, self).__init__(*args, **kwargs)

    def check_compiler_command(self, data):
        compiler_command = pickle.loads(data.get('compiler_command'))
        if get_compiler_name(self.assignment.program_language) != compiler_command[0]:
            self._errors['compiler_command'] = self.error_class(["Invalid compiler for {0} language .\
                    ".format(self.assignment.program_language)])
            del data['compiler_command']
            return
        for afile in compiler_command[2].split():
            if not is_valid(filename=afile, compiler=compiler_command[0]):
                self._errors['compiler_command'] = self.error_class(["Only {1} files are accepted for {0} compiler.\
                    ".format(compiler_command[0], " ".join(get_extension(compiler_command[0])))])
                del data['compiler_command']

    def check_program_files(self, data):
        self.__teachers_file = []
        if 'program_files' in self.changed_data:
            if data.get('program_files', ""):
                with Archive(fileobj=data['program_files']) as archive:
                    if archive.is_archive():
                        self.__teachers_file = [a.split("/")[-1] for a in archive.getfile_members()]
                    else:
                        if is_valid(filename=data['program_files'].name, compiler=pickle.loads(data['compiler_command'])[0]):
                            self.__teachers_file = [data['program_files'].name]
                        else:
                            self._errors['program_files'] = self.error_class(["This file was not valid."])
                            del data['program_files']
            else: # file is being deleted.
                pass
        else: # No change in file field. Check if file exist in database.
            if not hasattr(self, 'program_model'):
                return # Assignment is created without model solution.

            if not self.program_model.program_files: return # no file in database.

            with Archive(fileobj=self.program_model.program_files.file) as archive:
                if archive.is_archive():
                    self.__teachers_file = [a.split("/")[-1] for a in archive.getfile_members()]
                else:
                    if is_valid(filename=self.program_model.program_files.name, compiler=pickle.loads(data['compiler_command'])[0]):
                        self.__teachers_file = [self.program_model.program_files.name.split("/")[-1]]
                    else:
                        file_name = self.program_model.program_files.name.split("/")[-1]
                        self._errors['program_files'] = self.error_class(["File {0} is not valid. Please upload a valid file\
                            ".format(file_name)])
                        del data['program_files']

    def clean(self):
        cleaned_data = super(ProgramFormCNotE, self).clean()
        if self.errors: return cleaned_data

        self.check_compiler_command(cleaned_data)
        if self._errors: return cleaned_data

        self.check_program_files(cleaned_data)
        if self._errors: return cleaned_data

        compiler_command = pickle.loads(cleaned_data.get('compiler_command'))
        # file name to be compiled -- program files submitted by student should be in Teacher supplied tar.
        file_to_compile = set(compiler_command[2].split())
        students_file = cleaned_data.get('student_program_files', "")
        students_file = set(students_file.split())
        missing_file = file_to_compile - set(self.__teachers_file) - set(self.assignment.student_program_files.split())

        if missing_file:
            self._errors['program_files'] = self.error_class(["{0} is missing. It is one of the file in compilation command".format(" ".join(missing_file))])
            del cleaned_data['program_files']
        else:
            #Compile Program now.
            pass
        return cleaned_data


class ProgramFormCandE(forms.Form):
    #error_css_class = 'alert-error'
    #required_css_class = 'alert-error'
    PROGRAM_TYPES = (
                      ('Evaluate', 'Evaluate'),
                      ('Practice', 'Practice'),
                    )
    name = forms.CharField()
    program_type = forms.ChoiceField(choices=PROGRAM_TYPES)
    compiler_command = CompilerCommand(help_text="Give compiler flags in second field and file names in third field. File names can be any of the files from student submission provided in assignment details.\
                            If you provide other file names, upload those files in additional files below.",
                            required=False
                        )
    execution_command = ExecutionCommand(help_text="Give the execution command in this textbox",
                                        required=False)
    program_files = forms.FileField(
                        error_messages={'invalid': 'File was not a valid tar file.',},
                        required = False,
                        label="Additional Source Files",
                        help_text="Provide additional source files here.\
                                Accepted archives are tar, tar.gz, tar.bz2, zip."
                    )
    makefile = forms.FileField(
                    required=False,
                    help_text="Must be a text file."
                )
    description = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        kwargs['error_class']=DivErrorList
        super(ProgramFormCandE, self).__init__(*args, **kwargs)

    def check_compiler_command(self, data):
        compiler_command = pickle.loads(data.get('compiler_command'))
        if get_compiler_name(self.assignment.program_language) != compiler_command[0]:
            self._errors['compiler_command'] = self.error_class(["Invalid compiler for {0} language .\
                    ".format(self.assignment.program_language)])
            del data['compiler_command']
            return
        for afile in compiler_command[2].split():
            if not is_valid(filename=afile, compiler=compiler_command[0]):
                self._errors['compiler_command'] = self.error_class(["Only {1} files are accepted for {0} compiler.\
                    ".format(compiler_command[0], " ".join(get_extension(compiler_command[0])))])
                del data['compiler_command']

    def check_execution_command(self, data):
        execution_command = pickle.loads(data.get('execution_command'))
        if get_interpreter_name(self.assignment.program_language) != execution_command[0]:
            self._errors['execution_command'] = self.error_class(["Invalid interpreter for {0} language .\
                    ".format(self.assignment.program_language)])
            del data['execution_command']
            return
        for afile in execution_command[2].split():
            if not is_valid(filename=afile, interpreter=execution_command[0]):
                self._errors['execution_command'] = self.error_class(["Only {1} files are accepted for {0} interpreter.\
                    ".format(execution_command[0], " ".join(get_extension(execution_command[0])))])
                del data['execution_command']

    def check_program_files(self, data):
        self.__teachers_file = []
        if 'program_files' in self.changed_data:
            if data.get('program_files', ""):
                with Archive(fileobj=data['program_files']) as archive:
                    if archive.is_archive():
                        self.__teachers_file = [a.split("/")[-1] for a in archive.getfile_members()]
                    else:
                        if is_valid(filename=data['program_files'].name, compiler=pickle.loads(data['compiler_command'])[0]):
                            self.__teachers_file = [data['program_files'].name]
                        else:
                            self._errors['program_files'] = self.error_class(["This file was not valid."])
                            del data['program_files']
            else: # file is being deleted.
                pass
        else: # No change in file field. Check if file exist in database.
            if not hasattr(self, 'program_model'):
                return # Assignment is created without model solution.

            if not self.program_model.program_files: return # no file in database.

            with Archive(fileobj=self.program_model.program_files.file) as archive:
                if archive.is_archive():
                    self.__teachers_file = [a.split("/")[-1] for a in archive.getfile_members()]
                else:
                    if is_valid(filename=self.program_model.program_files.name, compiler=pickle.loads(data['compiler_command'])[0]):
                        self.__teachers_file = [self.program_model.program_files.name.split("/")[-1]]
                    else:
                        file_name = self.program_model.program_files.name.split("/")[-1]
                        self._errors['program_files'] = self.error_class(["File {0} is not valid. Please upload a valid file\
                            ".format(file_name)])
                        del data['program_files']

    def clean(self):
        cleaned_data = super(ProgramFormCandE, self).clean()
        if self.errors: return cleaned_data

        self.check_compiler_command(cleaned_data)
        if self._errors: return cleaned_data

        self.check_execution_command(cleaned_data)
        if self._errors: return cleaned_data

        self.check_program_files(cleaned_data)
        if self._errors: return cleaned_data

        compiler_command = pickle.loads(cleaned_data.get('compiler_command'))
        execution_command = pickle.loads(cleaned_data.get('execution_command'))
        # file name to be compiled -- program files submitted by student should be in Teacher supplied tar.
        file_to_compile = set(compiler_command[2].split())
        students_file = cleaned_data.get('student_program_files', "")
        students_file = set(students_file.split())
        missing_file = file_to_compile - set(self.__teachers_file) - set(self.assignment.student_program_files.split())

        if missing_file:
            self._errors['program_files'] = self.error_class(["{0} is missing. It is one of the file in compilation command".format(" ".join(missing_file))])
            del cleaned_data['program_files']
        else:
            #Compile Program now.
            pass
        return cleaned_data

class ProgramFormE(forms.Form):
    #error_css_class = 'alert-error'
    #required_css_class = 'alert-error'
    PROGRAM_TYPES = (
                      ('Evaluate', 'Evaluate'),
                      ('Practice', 'Practice'),
                    )
    name = forms.CharField()
    program_type = forms.ChoiceField(choices=PROGRAM_TYPES)
    execution_command = ExecutionCommand(help_text="Give the execution command in this textbox",
                                        required=False)
    program_files = forms.FileField(
                        error_messages={'invalid': 'File was not a valid tar file.',},
                        required = False,
                        label="Additional Source Files",
                        help_text="Provide additional source files here.\
                                Accepted archives are tar, tar.gz, tar.bz2, zip."
                    )
    makefile = forms.FileField(
                    required=False,
                    help_text="Must be a text file."
                )
    description = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        kwargs['error_class']=DivErrorList
        super(ProgramFormE, self).__init__(*args, **kwargs)

    def check_execution_command(self, data):
        execution_command = pickle.loads(data.get('execution_command'))
        if get_interpreter_name(self.assignment.program_language) != execution_command[0]:
            self._errors['execution_command'] = self.error_class(["Invalid interpreter for {0} language .\
                    ".format(self.assignment.program_language)])
            del data['execution_command']
            return
        for afile in execution_command[2].split():
            if not is_valid(filename=afile, interpreter=execution_command[0]):
                self._errors['execution_command'] = self.error_class(["Only {1} files are accepted for {0} interpreter.\
                    ".format(execution_command[0], " ".join(get_extension(execution_command[0])))])
                del data['execution_command']

    def check_program_files(self, data):
        self.__teachers_file = []
        if 'program_files' in self.changed_data:
            if data.get('program_files', ""):
                with Archive(fileobj=data['program_files']) as archive:
                    if archive.is_archive():
                        self.__teachers_file = [a.split("/")[-1] for a in archive.getfile_members()]
                    else:
                        if is_valid(filename=data['program_files'].name, interpreter=pickle.loads(data['execution_command'])[0]):
                            self.__teachers_file = [data['program_files'].name]
                        else:
                            self._errors['program_files'] = self.error_class(["This file was not valid."])
                            del data['program_files']
            else: # file is being deleted.
                pass
        else: # No change in file field. Check if file exist in database.
            if not hasattr(self, 'program_model'):
                return # Assignment is created without model solution.

            if not self.program_model.program_files: return # no file in database.

            with Archive(fileobj=self.program_model.program_files.file) as archive:
                if archive.is_archive():
                    self.__teachers_file = [a.split("/")[-1] for a in archive.getfile_members()]
                else:
                    if is_valid(filename=self.program_model.program_files.name, interpreter=pickle.loads(data['execution_command'])[0]):
                        self.__teachers_file = [self.program_model.program_files.name.split("/")[-1]]
                    else:
                        file_name = self.program_model.program_files.name.split("/")[-1]
                        self._errors['program_files'] = self.error_class(["File {0} is not valid. Please upload a valid file\
                            ".format(file_name)])
                        del data['program_files']

    def clean(self):
        cleaned_data = super(ProgramFormE, self).clean()

        if self.errors: return cleaned_data

        self.check_execution_command(cleaned_data)
        if self._errors: return cleaned_data

        self.check_program_files(cleaned_data)
        if self._errors: return cleaned_data

        execution_command = pickle.loads(cleaned_data.get('execution_command'))
        # file name to be compiled -- program files submitted by student should be in Teacher supplied tar.
        file_to_execute = set(execution_command[2].split())
        students_file = cleaned_data.get('student_program_files', "")
        students_file = set(students_file.split())
        missing_file = file_to_execute - set(self.__teachers_file) - set(self.assignment.student_program_files.split())

        if missing_file:
            self._errors['program_files'] = self.error_class(["{0} is missing. It is one of the file in execution command".format(" ".join(missing_file))])
            del cleaned_data['program_files']
        else:
            #Compile Program now.
            pass
        return cleaned_data

class TestcaseForm(forms.Form):
    name = forms.CharField(label="Testcase Name")
    command_line_args = forms.CharField(
                            label="Command Line Arguments",
                            required=False
                        )
    marks = forms.IntegerField(label="Marks", required=False)
    input_files = forms.FileField(
                    error_messages={'invalid': 'File was not a valid archive file.'},
                    required=False,
                    label="Input Files",
                    help_text="File used for program as input. Accepted archives are tar, tar.gz, tar.bz2, zip.",
                    allow_empty_file=True,
                )
    output_files = forms.FileField(
                    error_messages={'invalid': 'File was not a valid tar file.'},
                    required=False,
                    label="Output Files",
                    help_text="Expected output files produced by program. Accepted archives are tar, tar.gz, tar.bz2, zip.",
                    allow_empty_file=True,
                )
    description = forms.CharField(
                    widget=forms.Textarea,
                    required=False
                )

    def __init__(self, *args, **kwargs):
        kwargs['error_class'] = DivErrorList
        self.solution_ready = kwargs.pop('solution_ready', False)
        super(TestcaseForm, self).__init__(*args, **kwargs)

    def clean_input_files(self):
        data = self.cleaned_data
        # TODO: check if files are not tar it must be text file.
        return data['input_files']

    def clean_output_files(self):
        # TODO: check if files are not tar it must be text file.
        data = self.cleaned_data
        return data['output_files']

    def clean(self):
        cleaned_data = super(TestcaseForm, self).clean()
        if cleaned_data['marks'] is None: # cleaned_data['test_type'] == "Evaluate" and 
            self._errors['marks'] = self.error_class(['This field is required.'])

        # if solution executable is not available make output file required.
        if (not self.solution_ready) and cleaned_data['output_files'] is None:
            self._errors['output_files'] = self.error_class(['Solution code for this assignment is not available/broken please upload output files.'])

        return cleaned_data

class TestcaseForm2(forms.Form):
    std_in_file_name = forms.ChoiceField(
                            label="Select File for Standard input",
                            widget=forms.RadioSelect(),
                            choices=((("None", "None"),)),
                            help_text="Content will be supplied as standard input."
                        )
    std_out_file_name = forms.ChoiceField(
                            label="Select File for Standard output",
                            widget=forms.RadioSelect(),
                            choices=((("None", "None"),)),
                            help_text="File's content will used to compare standard output of program."
                        )

    def __init__(self, *args, **kwargs):
        in_file_name = kwargs.pop('in_file_choices', (("None", "None"),))
        out_file_name = kwargs.pop('out_file_choices', (("None", "None"),))

        kwargs['error_class'] = DivErrorList
        super(TestcaseForm2, self).__init__(*args, **kwargs)

        self.fields['std_in_file_name'].choices = in_file_name
        self.fields['std_out_file_name'].choices = out_file_name


class SafeExecForm(forms.Form):
    cpu_time = forms.IntegerField(label="CPU time", help_text='Default is 10 seconds.')
    clock_time = forms.IntegerField(label="Clock time", help_text='Default is 60 seconds.')
    memory = forms.IntegerField(label="Memory limit", help_text='Default is 32768 kbytes.')
    stack_size = forms.IntegerField(label="Stack size limit", help_text='Default is 8192 kbytes.')
    child_processes = forms.IntegerField(label="Number of child processes", help_text='Number of child processes it can create. Default is 0.')
    open_files = forms.IntegerField(
                            label="Number of open files",
                            help_text='Number of files the program can open. Default value is 512. Do not set this too\
                            low otherwise program will not be able to open shared libraries.'
                        )
    file_size = forms.IntegerField(label="Max file size", help_text='Maximum size of file the program can write. Default size is 0 kbytes.')
    env_vars = forms.CharField(label="Environment variables", required=False)
