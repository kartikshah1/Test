from django.shortcuts import get_object_or_404 #render_to_response
#from django.template import RequestContext
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
from django.http import HttpResponse
from django.utils import timezone

from assignments.models import Assignment, Program, Testcase
from upload.models import Upload

import os, tempfile, zipfile, StringIO, shutil


@login_required
def download_all_zipped(request, assignmentID):
    assignment = get_object_or_404(Assignment, pk=assignmentID)
    if not request.user == assignment.creater:
        return HttpResponseForbidden("Forbidden 403")

    all_submissions = Upload.objects.filter(assignment=assignment)
    filenames = [(a.owner.username, a.filePath.file.name) for a in all_submissions]

    try:
        zip_subdir = ""
        zip_filename = slugify(assignment.name + "-all-submissions") + '.zip'
        temp_dir = tempfile.mkdtemp(prefix="download_all")

        for s_name, fpath in filenames:
            _, fname = os.path.split(fpath)
            z_f = zipfile.ZipFile(os.path.join(temp_dir, s_name + '.zip'), "w")
            z_f.write(fpath, fname)
            z_f.close()
    
        # Open StringIO to grab in-memory ZIP contents
        s = StringIO.StringIO()
        zf = zipfile.ZipFile(s, "w")
    
        for fname in os.listdir(temp_dir):
            zip_path = os.path.join(zip_subdir, fname)
            zf.write(os.path.join(temp_dir, fname), zip_path)

        zf.close() # must close
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

    # Grab ZIP file from in-memory, make response with correct MIME-type
    resp = HttpResponse(s.getvalue(), mimetype = "application/x-zip-compressed")

    resp['Content-Length'] = s.tell()
    resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

    return resp

@login_required
def download_assignment_files(request, assignmentID):
    '''
    This view let student download all assignment data
    '''
    assignment = get_object_or_404(Assignment, pk=assignmentID)

    def file_name(fpath):
        return os.path.split(fpath)[1]

    if request.user == assignment.creater or timezone.now() > assignment.hard_deadline:
        programs = Program.objects.filter(assignment=assignment)
    else: # before deadline
        programs = Program.objects.filter(assignment=assignment, program_type='Practice')

    zip_filename = slugify(assignment.name + "-data") + '.zip'

    zip_dir = assignment.name
    s = StringIO.StringIO()
    zf = zipfile.ZipFile(s, "w")

    if assignment.document:
        zip_path = os.path.join(zip_dir, "documents", file_name(assignment.document.file.name))
        zf.write(assignment.document.file.name, zip_path)
    if assignment.helper_code:
        zip_path = os.path.join(zip_dir, "helper_code", file_name(assignment.helper_code.file.name))
        zf.write(assignment.helper_code.file.name, zip_path)

    for a_prgrm in programs:
        if a_prgrm.program_files:
            zip_path = os.path.join(zip_dir, a_prgrm.name, file_name(a_prgrm.program_files.file.name))
            zf.write(a_prgrm.program_files.file.name, zip_path)
        for test in Testcase.objects.filter(program=a_prgrm):
            sub_path = os.path.join(zip_dir, a_prgrm.name, test.name + "_" + str(test.id))
            if test.input_files:
                f_name = test.input_files.file.name
                zip_path = os.path.join(sub_path, file_name(f_name))
                zf.write(test.input_files.file.name, zip_path)
            if test.output_files:
                f_name = test.output_files.file.name
                zip_path = os.path.join(sub_path, file_name(f_name))
                zf.write(test.output_files.file.name, zip_path)
    zf.close()

    resp = HttpResponse(s.getvalue(), mimetype = "application/x-zip-compressed")
    resp['Content-Length'] = s.tell()
    resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

    return resp