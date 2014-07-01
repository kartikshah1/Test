from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from cribs.models import Crib
from cribs.models import Comment
from cribs.forms import CribForm, CommentForm
from assignments.models import Assignment


@login_required
def createCrib(request, assignmentID):
    assignment = get_object_or_404(Assignment, pk=assignmentID)        
    if request.method == 'POST':
        form = CribForm(request.POST)
        if form.is_valid():
            Crib.objects.get_or_create(
                        assignment=assignment,
                        created_by=request.user,
                        defaults=form.cleaned_data
                    )
            return HttpResponseRedirect(reverse('cribs.views.myCribs', kwargs={'assignmentID': assignment.id}))
    else:
        try:
            Crib.objects.get(assignment=assignment, created_by=request.user) # checking if there is already a crib.
            return HttpResponseRedirect(reverse('cribs.views.myCribs', kwargs={'assignmentID': assignment.id}))
        except Crib.DoesNotExist:
            form = CribForm() # render empty form if crib was not registered.

    return render_to_response(
            'cribs/create_crib.html',
            {'form': form, 'assignment': assignment},
            context_instance=RequestContext(request)
        )

@login_required
def myCribs(request, assignmentID):
    assignment = get_object_or_404(Assignment, pk=assignmentID)

    try:
        crib = Crib.objects.get(assignment=assignment, created_by=request.user)
    except Crib.DoesNotExist:
        crib = None
    comments = Comment.objects.filter(crib=crib)
    form = CommentForm()
    return render_to_response(
            'cribs/my_crib.html',
            {'crib': crib, 'form': form, 'comments': comments,
             'assignment': assignment,},
            context_instance=RequestContext(request)
        )

@login_required
def allCribs(request, assignmentID):
    assignment = get_object_or_404(Assignment, pk=assignmentID)
    allCribs = Crib.objects.filter(assignment=assignment)
    return render_to_response(
            'cribs/all_cribs.html',
            {'assignment': assignment, 'allcribs': allCribs},
            context_instance=RequestContext(request)
        )

@login_required
def cribDetail(request, cribID):
    crib = get_object_or_404(Crib, pk=cribID)
    comments = Comment.objects.filter(crib=crib)
    form = CommentForm()
    return render_to_response(
            'cribs/my_crib.html',
            {'crib': crib, 'form': form, 'comments': comments},
            context_instance=RequestContext(request)
        )

@login_required
def editCrib(request, cribID):
    pass

@login_required
def closeCrib(request, cribID):
    pass

@login_required
def reopenCrib(request, cribID):
    pass

@login_required
def postComment(request, cribID):
    # TODO: Implement in Ajax.
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(**form.cleaned_data)
            comment.posted_by = request.user
            comment.crib = get_object_or_404(Crib, pk=cribID)
            comment.save()
        return HttpResponse("Saved! (Later this will be implemented with Ajax. Hit back button and refresh page to see your comment.)")

@login_required
def editComment(request, commentID):
    pass