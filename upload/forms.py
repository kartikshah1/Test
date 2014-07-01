from django import forms

from utils.archives import get_file_name_list, get_missing_files

# This form is used to upload student submissions.
# The student uploads on the details page of the assignment is collected by this form and using this form we create new instance of upload objects.
class UploadForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file',
        error_messages={
                        'invalid': 'File was not a valid tar file.',
                        'missing_files': 'Missing files.',
                        },
    )

    def __init__(self, *args, **kwargs):
        self.assignment_model_obj = kwargs.pop('assignment_model_obj', "")
        super(UploadForm, self).__init__(*args, **kwargs)

    # This function checks if the upload object has all the needed files.
    def clean_docfile(self):
        # Get all files that should be submitted by student from all programs of given AssignmentID.
        data = self.cleaned_data
        submitted_files = get_file_name_list(fileobj=data['docfile'])
        progrm_files_name = self.assignment_model_obj.student_program_files.split()

        # Check if tarfile contains all of these.
        missing_files = get_missing_files(progrm_files_name, fileobj=data['docfile'])

        # If there are missing files raise error and display all missing files.
        if missing_files:
            self.fields['docfile'].error_messages["docfile"] = "There were missing files."
            if set(submitted_files) >= set(progrm_files_name):
                error_msg = "Directory structure is incorrect! Put all source files in single directory only.\
                Nested directories are not allowed."
            else:
                error_msg = 'Missing files!. Your SUBMISSION contains "{0}" and we expect you to submit "{1}"\
                            Please upload again with missing files "{2}"'.format(" ".join(submitted_files),\
                            " ".join(progrm_files_name), " ".join(missing_files))
            raise forms.ValidationError(error_msg)
        return data['docfile']
