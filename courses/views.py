from django.http import HttpResponseRedirect, HttpResponse
from django.http import HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.forms import model_to_dict
from django.template import RequestContext
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import json
'''
from courses.models import CourseForm
from courses.forms import RoleForm, JoinCourseForm
from courses.models import Course
from courses.models import Role
'''
from courseware.views import student_course_list

@login_required
def index(request):
    '''
    if request.method == 'POST':
        join_course_form = JoinCourseForm(request.POST)
        join_course_form.current_user = request.user
        join_course_form.course_class = Course

        if join_course_form.is_valid():
            role = Role(
                        user = request.user,
                        course = get_object_or_404(Course, name=request.POST.get('name_or_id')),
                        role = join_course_form.cleaned_data.get('role')
                    )
            role.save()
            return HttpResponseRedirect(reverse('courses.views.index'))
        else:
            a=2
    else:
        join_course_form = JoinCourseForm()
    '''
    allcourses = student_course_list(request)
    #courseCreated = Course.objects.filter(creater=request.user)
    #courseJoined = Role.objects.filter(user=request.user, role='S')

    return render_to_response(
                'courses/courses.html',
                {'allcourses': allcourses},
                context_instance=RequestContext(request)
            )

'''
@login_required
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            newCourse = Course(**form.cleaned_data)
            newCourse.creater = request.user
            newCourse.save()
            return HttpResponseRedirect(reverse('courses.views.index'))
    else:
        form = CourseForm()

    #courseJoined = Course
    return render_to_response(
                'courses/create_course.html',
                {'form':form},
                context_instance=RequestContext(request)
            )

@login_required
def all_courses(request):
    courses = Course.objects.all()[:30]
    return render_to_response(
                'courses/all_courses.html',
                {'courses': courses},
                context_instance=RequestContext(request)
            )


@login_required
def editCourse(request, courseid):
    course = get_object_or_404(Course, pk=courseid)
    if not request.user == course.creater:
        return HttpResponseForbidden("Forbidden 403")

    if request.method == 'POST':
        form = CourseForm(request.POST, initial=model_to_dict(course))
        if form.is_valid():
            for key in form.cleaned_data.keys():
                setattr(course, key, form.cleaned_data[key])
            course.save()
            return HttpResponseRedirect(reverse('assignments_index', kwargs={'courseID': courseid}))
    else:
        form = CourseForm(initial=model_to_dict(course))
    return render_to_response(
                'courses/edit_course.html',
                {'form':form, 'course': course,},
                context_instance=RequestContext(request)
            )

@login_required
def delete_course(request, courseid):
    course = get_object_or_404(Course, pk=courseid)
    if not request.user == course.creater:
        return HttpResponseForbidden("Forbidden 403")

    course.delete()
    return HttpResponseRedirect(reverse('courses_index'))

@login_required
def courseInfo(request, courseid):
    course = get_object_or_404(Course, pk=courseid)
    #Display course information in main div. In side bar show Course name and a form to join this course
    #if it not joined already. We can also show unregister button for those who have registered.
    return render_to_response(
                'courses/courseDetails.html',
                {'course': course},
                context_instance=RequestContext(request)
            )

@login_required
def joinCourse(request, courseid):
    #return a page with sidebar updated. now show leave course button.#
    course = get_object_or_404(Course, pk=courseid)
    Role.objects.get_or_create(
                        user=request.user,
                        course=course,
                        role='S'
                    )
    return HttpResponseRedirect(reverse('assignments.views.index', kwargs={'courseID': courseid}))

@login_required
def leaveCourse(request, courseid):
    # TODO: Implement leaveCourse method.
	#return a page with sidebar updated. now show join course button.#
    course = get_object_or_404(Course, pk=courseid)
    try:
        role_obj = Role.objects.get(user=request.user, course=course, role='S')
        role_obj.delete()
    except Role.DoesNotExist:
        pass
    return HttpResponseRedirect(reverse('assignments.views.index', kwargs={'courseID': courseid}))

@login_required
def searchCourse(request):
    #This view is to serve ajax auto-complete request only.
    if request.is_ajax():
        term = request.GET.get('term', '')
        courses = Course.objects.filter(Q(name__icontains=term) | Q(code__icontains=term))[:10]
        results = []
        for course in courses:
            course_json = {}
            course_json['id'] = course.id
            course_json['label'] = course.id + ", " + course.title
            course_json['value'] = course.title
            results.append(course_json)
        data = json.dumps(results)
    else:
        data = 'fail'

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
    
'''