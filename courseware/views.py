"""
This file basically contains viewsets for the courseware API

Category API:
    - List, Create, Update, Retrieve, Destroy, Partial Update Category
    - Get all courses in a category
    - Add a course in that category

Course API:
    - Retrieve, Update, Partial Update, Destroy info of a course
    - Retrieve, Update, Partial update courseinfo
    - List all the students in a course with their history
    - Create, update, parital update, Retrieve  course history
    - List all concepts in a course
    - Create, Retrieve, Update, Partial Update a concept

CourseHistory API:
    - List all the concept history in that coursehistory

Concept API:
    - Destroy a concept
    - Retrieve, Update Concept history
    - playlist
    - Create a learning element
"""

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from elearning_academy.permissions import InInstructorOrContentDeveloperMode, get_mode
from elearning_academy.permissions import InInstructorMode, InContentDeveloperMode

from courseware.models import Course, CourseHistory
from courseware.vsserializers.course import CourseSerializer, CourseInfoSerializer

from rest_framework import status

from django.http import HttpResponse
import json
from django.utils import timezone

inInstructorOrContentDeveloperModeObject = InInstructorOrContentDeveloperMode()
inInstructorModeObject = InInstructorMode()
inContentDeveloperModeObject = InContentDeveloperMode()


def parent_categories(request):
    """
    Serves parent_categories.html template
    """
    context = {"request": request}
    return render(request, "category/parent_categories.html", context)


def categories(request, pk):
    """
    Serves categories.html template
    """
    context = {"request": request, "pk": pk}
    return render(request, "category/categories.html", context)


@login_required
def add_course(request):
    """
    Serves course_admin.html template
    """
    if request.user.get_profile().is_instructor:
        context = {"request": request}
        return render(request, "course/course_admin.html", context)
    else:
        context = {
            "request": request,
            "error": "You have to be an instructor to add a course."
            }
        return render(request, "error.html", context)


def courses(request, pk):
    """Serves categories courses"""
    context = {"request": request, 'pk': pk}
    return render(request, "category/courses.html", context)


@login_required
def course(request, pk=None, ref=None):
    """Serves a course main page"""
    _course = get_object_or_404(Course, pk=pk)
    context = {"request": request, "course": _course}
    if ref is not None and len(ref) > 0:
        context["ref"] = ref
    else:
        context["ref"] = "-1"
    mode = get_mode(request)
    history = CourseHistory.objects.filter(user=request.user, course=_course, active='A')

    if mode == 'I' or mode == 'C':
        if len(history) > 0:
            if history[0].is_owner:
                return render(request, "content_developer/course.html", context)
        return render(request, "student/course.html", context)
    #elif mode == 'S':
    else:
        if len(history) > 0:
            return render(request, "student/course.html", context)
        course_data = CourseSerializer(_course).data
        if course_data['course_info']['start_time']:
            s_date = course_data['course_info']['start_time'].strftime('%d %b,%Y')
            course_data['course_info']['start_time'] = s_date
        if course_data['course_info']['end_time']:
            e_date = course_data['course_info']['end_time'].strftime('%d %b,%Y')
            course_data['course_info']['end_time'] = e_date
        if course_data['course_info']['end_enrollment_date']:
            end_e_date = course_data['course_info']['end_enrollment_date'].strftime('%d %b,%Y')
            course_data['course_info']['end_enrollment_date'] = end_e_date
        context = {
            "request": request,
            "title": course_data['title'],
            "course": json.dumps(course_data),
            "course_info": json.dumps(course_data['course_info'])
        }
        return render(request, "course/public_course_info.html", context)
    return HttpResponse("Forbidden", status.HTTP_403_FORBIDDEN)


@login_required
def syllabus(request, pk=None):
    """Serves a course main page"""
    _course = get_object_or_404(Course, pk=pk)
    context = {"request": request, "course": _course}
    if request.user.get_profile().is_instructor:
        return render(request, "instructor/syllabus.html", context)
    else:
        context = {
            "request": request,
            "error": "You have to be an instructor to see syllabus."
        }
        return render(request, "error.html", context)


@login_required
def student_courses(request):
    """
        Serve enrolled course list for a student
    """
    response = student_course_list(request)
    context = {"data": json.dumps(response)}
    return render(request, "student/my_courses.html", context)


@login_required
def instructor_courses(request):
    """
        Added by vinayak, needs to be verified from writer of instructor_course_list()
        Serve offered course list for a instructor (?)
    """
    if inInstructorModeObject.has_permission(request, None):
        response = instructor_course_list(request)
        context = {"data": json.dumps(response)}
        return render(request, "instructor/my_offerings.html", context)
    else:
        context = {
            "request": request,
            "error": "Invalid Access. Change mode or contact admin"
        }
        return render(request, "error.html", context)


@login_required
def content_developer_courses(request):
    """
        Serves textbook course list for a content developer
    """
    if inContentDeveloperModeObject.has_permission(request, None):
        response = content_developer_course_list(request)
        context = {"data": json.dumps(response)}
        #: Need to change the page for content developer courses
        print "New Textbook Page"
        return render(request, "content_developer/my_textbooks.html", context)
    else:
        context = {
            "request": request,
            "error": "Invalid Access.Change mode or contact admin"
        }
        return render(request, "error.html", context)


@login_required
def mycourselist(request):
    """
        Obselete. Purpose not clear
        Serves the enrolled course list for a student
    """
    mode = get_mode(request)
    if mode == 'I':
        return instructor_courses(request)
    elif mode == 'C':
        return content_developer_courses(request)
    #elif mode == 'S':
    #    return student_courses(request)
    #return HttpResponse("Forbidden", status.HTTP_403_FORBIDDEN)
    else:
        return student_courses(request)


@login_required
def content_developer_course_list(request):
    """
        Return a list of courses being developed by user as a content developer
    """
    date_format = "%d %b, %Y"
    history_list = CourseHistory.objects.filter(user=request.user, is_owner=True, course__type='T')
    all_courses = []
    for history in history_list:
        if history.course.type == 'T':
            all_courses.append(history.course)
    all_courses_data = [CourseSerializer(c).data for c in all_courses]
    cur_datetime = timezone.now().date()
    ##Course Current Status in coursetag.
    ##    1 => active
    ##    2 => Future
    ##    3 => past
    all_coursetag = []
    start_date = []
    all_course_progress = []
    for c_data in all_courses_data:
        c_info = c_data['course_info']
        if (c_info['end_time'] is None or cur_datetime < c_info['start_time']):
            tag = 2
        elif (cur_datetime > c_info['end_time']):
            tag = 3
        else:
            tag = 1
        all_coursetag.append({"is_published": c_info['is_published'], "coursetag": tag})

        if c_info['end_time'] is None or c_info['start_time'] is None:
            progress = 0
        else:
            elapsed_time = (cur_datetime - c_info['start_time']).days
            total_time = (c_info['end_time'] - c_info['start_time']).days
            progress = (float)(100 * elapsed_time / total_time)
        if progress > 100:
            progress = 100
        elif progress < 0:
            progress = 0
        all_course_progress.append({"progress": progress})

        if (c_info['start_time'] is not None):
            s_date = c_info['start_time'].strftime(date_format)
            c_data['course_info']['start_time'] = s_date
        else:
            s_date = "Not Decided"
        if (c_info['end_time'] is not None):
            e_date = c_info['end_time'].strftime(date_format)
            c_data['course_info']['end_time'] = e_date
        else:
            e_date = "Not Decided"
        start_date.append({
            "start_date": s_date,
            "end_date": e_date,
            "start_time": s_date,
            "end_time": e_date
        })

        if (c_info['end_enrollment_date']):
            end_e_date = c_info['end_enrollment_date'].strftime(date_format)
            c_data['course_info']['end_enrollment_date'] = end_e_date

    response = []
    for i in range(len(all_courses_data)):
        response.append((dict(all_course_progress[i].items() + all_coursetag[i].items() +
                         all_courses_data[i].items() + start_date[i].items())))

    response = sort_my_courses(response)
    return response


@login_required
def instructor_course_list(request):
    """
        Return a list of courses which are offered by the user as instructor
    """
    date_format = "%d %b, %Y"
    history_list = CourseHistory.objects.filter(user=request.user, is_owner=True, course__type='O')
    all_courses = []
    for history in history_list:
        if history.course.type == 'O':
            all_courses.append(history.course)
    all_courses_data = [CourseSerializer(c).data for c in all_courses]
    cur_datetime = timezone.now().date()
    ##Course Current Status in coursetag.
    ##    1 => active
    ##    2 => Future
    ##    3 => past
    all_coursetag = []
    start_date = []
    all_course_progress = []
    for c_data in all_courses_data:
        c_info = c_data['course_info']
        if (c_info['end_time'] is None or cur_datetime < c_info['start_time']):
            tag = 2
        elif (cur_datetime > c_info['end_time']):
            tag = 3
        else:
            tag = 1
        all_coursetag.append({"is_published": c_info['is_published'], "coursetag": tag})

        if c_info['end_time'] is None or c_info['start_time'] is None:
            progress = 0
        else:
            elapsed_time = (cur_datetime - c_info['start_time']).days
            total_time = (c_info['end_time'] - c_info['start_time']).days
            progress = (float)(100 * elapsed_time / total_time)
        if progress > 100:
            progress = 100
        elif progress < 0:
            progress = 0
        all_course_progress.append({"progress": progress})

        if (c_info['start_time'] is not None):
            s_date = c_info['start_time'].strftime(date_format)
            c_data['course_info']['start_time'] = s_date
        else:
            s_date = "Not Decided"
        if (c_info['end_time'] is not None):
            e_date = c_info['end_time'].strftime(date_format)
            c_data['course_info']['end_time'] = e_date
        else:
            e_date = "Not Decided"
        start_date.append({
            "start_date": s_date,
            "end_date": e_date,
            "start_time": s_date,
            "end_time": e_date
        })

        if c_info['end_enrollment_date']:
            end_e_date = c_info['end_enrollment_date'].strftime(date_format)
            c_data['course_info']['end_enrollment_date'] = end_e_date

    response = []
    for i in range(len(all_courses_data)):
        response.append((dict(all_course_progress[i].items() + all_coursetag[i].items() +
                         all_courses_data[i].items() + start_date[i].items())))

    response = sort_my_courses(response)
    return response


@login_required
def student_course_list(request):
    """
        Return a list of all courses where the student is enrolled
    """
    date_format = "%d %b, %Y"
    history_list = CourseHistory.objects.filter(user=request.user, active='A', is_owner=False)
    all_courses = []
    for history in history_list:
        if history.course.type == 'O':
            all_courses.append(history.course)
    all_courses_data = [CourseSerializer(c).data for c in all_courses]
    cur_datetime = timezone.now().date()
    ##Course Current Status in coursetag.
    ##    1 => active
    ##    2 => Future
    ##    3 => past
    all_coursetag = []
    start_date = []
    all_course_progress = []
    for c_data in all_courses_data:
        c_info = c_data['course_info']
        if (c_info['end_time'] is None or cur_datetime < c_info['start_time']):
            tag = 2
        elif (cur_datetime > c_info['end_time']):
            tag = 3
        else:
            tag = 1
        all_coursetag.append({"is_published": c_info['is_published'], "coursetag": tag})

        if c_info['end_time'] is None or c_info['start_time'] is None:
            progress = 0
        else:
            elapsed_time = (cur_datetime - c_info['start_time']).days
            total_time = (c_info['end_time'] - c_info['start_time']).days
            progress = (float)(100 * elapsed_time / total_time)
        if progress > 100:
            progress = 100
        elif progress < 0:
            progress = 0
        all_course_progress.append({"progress": progress})

        if (c_info['start_time'] is not None):
            s_date = c_info['start_time'].strftime(date_format)
            c_data['course_info']['start_time'] = s_date
        else:
            s_date = "Not Decided"
        if (c_info['end_time'] is not None):
            e_date = c_info['end_time'].strftime(date_format)
            c_data['course_info']['end_time'] = e_date
        else:
            e_date = "Not Decided"
        start_date.append({
            "start_date": s_date,
            "end_date": e_date,
            "start_time": s_date,
            "end_time": e_date
        })

        if c_info['end_enrollment_date']:
            end_e_date = c_info['end_enrollment_date'].strftime(date_format)
            c_data['course_info']['end_enrollment_date'] = end_e_date

    response = []
    for i in range(len(all_courses_data)):
        response.append((dict(all_course_progress[i].items() + all_coursetag[i].items() +
                         all_courses_data[i].items() + start_date[i].items())))

    response = sort_my_courses(response)
    return response


def coursecmp(x, y):
    if(x['coursetag'] > y['coursetag']):
        return 1
    elif(x['coursetag'] < y['coursetag']):
        return -1
    elif (x['start_time'] is not None) and (y['start_time'] is not None) and (x['start_time'] < y['start_time']):
        return -1
    return 1


def sort_my_courses(response):
    #sorted_master_list = sorted(response, key=itemgetter('coursetag'))
    sorted_master_list = sorted(response, cmp=coursecmp)
    return sorted_master_list


def dateToString(start_date):
    """ Convert the DateField to a printable string """
    return start_date.strftime("%d %B")


def paginated_serializer(request=None, queryset=None, serializer=None, paginate_by=5):
    """
    Returns the serializer containing objects corresponding to paginated page.
    Abstract Functionality can be used by all.
    """
    paginator = Paginator(queryset, paginate_by)
    page = request.QUERY_PARAMS.get('page')
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        items = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999),
        # deliver last page of results.
        items = paginator.page(paginator.num_pages)
    serializer_context = {'request': request}
    return serializer(items, context=serializer_context)


def to_do(request):
    """
        Functionality to be added
    """
    return HttpResponse("Functionality to be added")


def instructor_course_list_old(request):
    histories = CourseHistory.objects.filter(user=request.user, is_owner=True, course__type='O')
    my_courses = [history.course for history in histories]
    my_courses = [CourseSerializer(course).data for course in my_courses]

    my_courses = [history.course for history in histories]
    my_courses_info = [CourseInfoSerializer(course.course_info).data for course in my_courses]
    current_datetime = timezone.now().date()
    # Calculating CourseTag for all the courses. Coursetag = 1 => active course, coursetag = 2 =>
    # future course
    # and coursetag = 3 => past course
    coursetag = [{"is_published": element['is_published'], "coursetag": 2 if (element['end_time'] == None or current_datetime < element['start_time'])  else 3 if (current_datetime > element['end_time']) else 1} for element in my_courses_info]
    # Calculating printable dates
    start_date = [{"start_date": dateToString(element['start_time']) if element['start_time'] != None else "Not Decided" , "end_date": dateToString(element['end_time']) if element['end_time'] != None else "Not Decided"} for element in my_courses_info]
    # Calculating the progress of every course on teh basis of current date, course start date and course end date
    my_courses_progress = [0 if (element['end_time'] == None or element['start_time'] == None) else (float) (100*(current_datetime - element['start_time']).days/(element['end_time']-element['start_time']).days) for element in my_courses_info]
    my_courses_progress = [{"progress": element if(element <= 100) else 100} for element in my_courses_progress]

    my_courses = [CourseSerializer(course).data for course in my_courses]
    # Appending the course progress and coursetag to the response
    response = [(dict(my_courses_progress[i].items() + my_courses[i].items() + coursetag[i].items() + start_date[i].items())) for i in range(len(my_courses))]
    # Converting teh start and end date of courses to string to make it JSOn serializable
    my_courses_info = [{"start_time": str(element['start_time']), "end_time" : str(element['end_time'])} for element in my_courses_info]
    # Appending the course end and start date to the response
    response = [(dict(response[i].items() + my_courses_info[i].items())) for i in range(len(response))]
    # Sorting the results
    response = sort_my_courses(response)
    return response
