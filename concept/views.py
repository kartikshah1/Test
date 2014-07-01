"""
Views for Concept API
"""


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from elearning_academy.permissions import InInstructorOrContentDeveloperMode
from courseware.permissions import IsOwner
from courseware.models import Concept


@login_required
def view_concept(request, concept_id):
    """
        View Concept Page
    """
    concept = get_object_or_404(Concept, pk=concept_id)
    inInstructorOrContentDeveloperModeObject = InInstructorOrContentDeveloperMode()
    isOwnerObj = IsOwner()
    if inInstructorOrContentDeveloperModeObject.has_permission(request, None):
        return view_content_developer(request, concept_id)
    elif (concept.is_published or
          isOwnerObj.has_object_permission(request=request, obj=concept.group.course, view=None)):
        return view_student(request, concept_id)
    else:
        return render(request, 'error.html', {'error': 'Concept does not exist !'})


@login_required
def view_student(request, concept_id):
    """ Course Progress of Student """
    return render(request, 'concept/student.html', {'conceptId': concept_id})


@login_required
def view_content_developer(request, concept_id):
    """ Concept edit page for content developer """
    return render(request, 'concept/content_developer.html', {'conceptId': concept_id})
