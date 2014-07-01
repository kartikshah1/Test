from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.defaultfilters import slugify

from assignments.models import Assignment, Program
from evaluate.models import AssignmentResults
from upload.models import Upload
from upload.forms import UploadForm
from django.http import HttpResponse

import os, tempfile, zipfile, StringIO, shutil

@login_required
def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Upload(filePath = request.FILES['docfile'])
            newdoc.owner = request.user

            #Overwrite file if already exist.
            '''documents = Upload.objects.filter(owner=request.user)
            if documents:
                #print os.path.join(MEDIA_ROOT, documents[0].filePath.name)
                os.remove(os.path.join(MEDIA_ROOT, documents[0].filePath.name))
                documents.delete()'''
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('upload.views.upload'))
    else:
        form = UploadForm()

    documents = Upload.objects.filter(owner=request.user)
    return render_to_response(
                'upload/upload.html',
                {'form':form, 'documents': documents},
                context_instance=RequestContext(request)
            )


@login_required
def uploadAssignment(request, assignmentID):
    if request.method == 'POST':
        assignment = get_object_or_404(Assignment, pk=assignmentID)
        form = UploadForm(request.POST, request.FILES, assignment_model_obj=assignment)
        if form.is_valid():
            newUpload = Upload(
                               owner = request.user,
                               assignment = assignment,
                               filePath = request.FILES['docfile']
                            )
            newUpload.save()
        else:
            return form.errors
        #return HttpResponseRedirect(reverse('assignments_details', kwargs={'assignmentID':assignmentID, 'form': form}))

@login_required
def showAllSubmissions(request, assignmentID):
    if request.method == 'GET':
        assignment=get_object_or_404(Assignment, pk=assignmentID)

        if not request.user == assignment.creater:
            return HttpResponseForbidden('<h1>Forbidden 403</h1>')

        allSubmission = Upload.objects.filter(assignment=assignment).order_by("-uploaded_on")
        paginator = Paginator(allSubmission, 20)
        page = request.GET.get('page')
    
        try:
            submission = paginator.page(page)
        except PageNotAnInteger:
            submission = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            submission = paginator.page(paginator.num_pages)
    
        disable = False
        if submission:
            programs = Program.objects.filter(assignment=assignment)
            for aprogram in programs:
                if not aprogram.is_sane:
                    disable = True
                    break
        assignment_results = AssignmentResults.objects.filter(submission__in=submission)
        #submisions_with_result = [(a.submission, a) for a in assignment_results]
        for a_submission in submission:
            marks = [s.get_marks() for s in assignment_results if s.submission == a_submission]
            if marks: # means a_submission has result
                a_submission.result_available_v = True
                a_submission.marks_v = marks[0]

        return render_to_response(
                    'upload/allSubmissions.html',
                    {'allSubmission': submission, 'assignment': assignment, 'disable': disable},
                    context_instance=RequestContext(request)
                )
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')

@login_required
def download_all_zipped(request, assignmentID):
    assignment = get_object_or_404(Assignment, pk=assignmentID)
    if not request.user == assignment.creater:
        return HttpResponseForbidden("Forbidden 403")

    all_submissions = Upload.objects.filter(assignment=assignment)
    filenames = [(a.owner.username, a.filePath.file.name) for a in all_submissions]
    temp_dir = None
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
    except Exception as e:
        print e.message
    finally:
        if temp_dir:
            shutil.rmtree(temp_dir, ignore_errors=True)

    # Grab ZIP file from in-memory, make response with correct MIME-type
    resp = HttpResponse(s.getvalue(), mimetype = "application/x-zip-compressed")

    resp['Content-Length'] = s.tell()
    resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

    return resp

@login_required
def my_submissions(request, courseID):
    '''
    List all submission of a current user for a given course.
    '''
    course = get_object_or_404(Course,  pk=courseID)

    all_assignments = Assignment.objects.filter(course=course)
    all_uploads = Upload.objects.filter(assignment__in=all_assignments, owner=request.user).order_by("-uploaded_on")

    return render_to_response(
                       'upload/my_submissions.html',
                       {'course': course, 'all_uploads': all_uploads},
                       context_instance=RequestContext(request)
                )