"""
    This file contain the viewsets for the course, offering, courseinfo and CourseHistory models.
    Functionality Provided:
    Course:
        + Add - (IsDeveloper)
        + Update, PartialUpdate, Delete - (IsCourseDeveloper)
        + List - (everyone allowed)
        + Retrieve - (IsRegisteredOrAnyInstructor)

        - add_page - (IsOwner)
        - pages - (IsRegisteredOrAnyInstructor)
        - reorder_pages - (IsOwner)

        - courseInfo - (None)
        - pending_students, approve - (IsOwner)
        - register - (None)
        - deregister - (None)

        - progress - (IsRegistered)
        - get_all_marks - (IsOwner)

        - groups - (IsRegisteredOrAnyInstructor)
        - add_group - (IsOwner)
        - reorder_groups - (IsOwner)

    Offering:
        + Add: (IsInstructor)
        + Update, PartialUpdate, Delete: (IsCourseInstructor)
        + List: (None)
        + Retrieve: (IsRegistered)

        - get_shortlisted_courses - (IsOwner)
        - shortlist_course - (IsOwner)
"""

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from courseware.models import Course, Offering, CourseInfo, \
    CourseHistory, Group, ConceptHistory
from courseware.vsserializers.course import CourseSerializer, \
    CourseHistorySerializer, OfferingSerializer, CourseInfoSerializer
from courseware.serializers import GroupSerializer, AddGroupSerializer, \
    ConceptHistorySerializer
from courseware import playlist
from courseware.permissions import IsInstructorOrReadOnly, IsRegistered, \
    IsContentDeveloperOrReadOnly, IsOwnerOrReadOnly, IsOwner

from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import link, action
from rest_framework.permissions import AllowAny
from discussion_forum.models import UserSetting
from document.models import Document
from document.serializers import DocumentSerializer

from discussion_forum.models import Tag
from elearning_academy.permissions import get_mode

import ast


class CourseViewSet(viewsets.ModelViewSet):

    """
    ViewSet for Course Class
    """
    model = Course
    serializer_class = CourseSerializer
    permission_classes = [IsContentDeveloperOrReadOnly]

    def get_queryset(self):
        """
            Optionally restricts the returned courses to a given category.
        """
        queryset = Course.objects.all()
        category = self.request.QUERY_PARAMS.get('category', None)
        if category is not None:
            queryset = queryset.filter(category__id=category)
        return queryset

    def list(self, request):
        """
            List all the courses for q queryset
        """
        mode = get_mode(request)
        queryset = Course.objects.all()
        category = self.request.QUERY_PARAMS.get('category', None)
        if category is not None:
            queryset = queryset.filter(category__id=category)
        if mode == 'I':
            queryset = queryset.filter(type='T')
        elif mode == 'C':
            queryset = queryset.filter()
        else:
            queryset = queryset.filter(
                type='O', course_info__is_published=True)
        serializer = CourseSerializer(queryset)
        response = {
            "count": len(serializer.data),
            "next": "null",
            "previous": "null",
            "results": serializer.data
        }
        return Response(response)

    def create(self, request, *args):
        """
        Function for creating a course in a category
        """
        serializer = CourseSerializer(data=request.DATA, files=request.FILES)
        if serializer.is_valid():
            serializer.save()
            coursehistory = CourseHistory(
                user=request.user,
                course=serializer.object,
                active='A',
                is_owner=True
            )
            coursehistory.save()

            # Usersetting for the discussion forum
            usersetting = UserSetting(
                user=request.user,
                forum=serializer.object.forum, super_user=True, moderator=True, badge='IN')
            usersetting.save()
            # send for approval now
            return Response(serializer.data)
        else:
            content = serializer.errors
            return Response(content, status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'],
            permission_classes=((IsOwnerOrReadOnly,)),
            serializer_class=DocumentSerializer)
    def add_page(self, request, pk=None):
        _course = get_object_or_404(Course, pk=pk)
        self.check_object_permissions(request, _course)
        serializer = DocumentSerializer(data=request.DATA)
        if serializer.is_valid():
            document = Document(
                title=serializer.data['title'],
                is_heading=True,
                description=serializer.data['description']
            )
            document.save()
            _course.pages.add(document)
            _course.page_playlist = playlist.append(
                document.id, _course.page_playlist)
            _course.save()
            return Response(DocumentSerializer(document).data)
        else:
            content = serializer.errors
            return Response(content, status.HTTP_400_BAD_REQUEST)

    @link(permission_classes=((IsOwnerOrReadOnly,)))
    def pages(self, request, pk=None):
        _course = get_object_or_404(Course, pk=pk)
        self.check_object_permissions(request, _course)
        pages = _course.pages.all()
        serializer = DocumentSerializer(pages, many=True)
        page_playlist = playlist.to_array(_course.page_playlist)
        N = len(page_playlist)
        ordered_data = [""] * N
        for i in range(N):
            ordered_data[i] = serializer.data[page_playlist[i][1]]
        return Response(ordered_data)

    @action(
        methods=['PATCH'],
        permission_classes=((IsOwnerOrReadOnly,)),
        serializer_class=CourseSerializer)
    def reorder_pages(self, request, pk=None):
        _course = get_object_or_404(Course, pk=pk)
        self.check_object_permissions(request, _course)
        print request.DATA
        myplaylist = request.DATA['playlist']
        print myplaylist
        newplaylist = playlist.is_valid(myplaylist, _course.page_playlist)
        if newplaylist is not False:
            _course.page_playlist = newplaylist
            _course.save()
            return Response(_course.page_playlist)
        else:
            content = "Given order data does not have the correct format"
            return Response(content, status.HTTP_404_NOT_FOUND)

    @link()
    def courseInfo(self, request, pk=None):
        """
            Function to get courseinfo, anyone can access courseinfo as it is public.
            TODO: to add permission to avoid giving info to for a unpublished course.
        """
        _course = get_object_or_404(Course, pk=pk)
        #self.check_object_permissions(request, _course)
        courseinfo = CourseInfo.objects.get(CourseInfo_Course=_course)
        serializer = CourseInfoSerializer(courseinfo)
        return Response(serializer.data)

    @action(methods=['POST'], permission_classes=((IsOwner, )))
    def publish(self, request, pk=None):
        """
            Publish a course so that students can see it for enrollment
        """
        course = get_object_or_404(Course, pk=pk)
        self.check_object_permissions(request, course)
        courseinfo = course.course_info
        if courseinfo.is_published:
            return Response({"error": "Cannot unpublish course"}, status.HTTP_400_BAD_REQUEST)
        courseinfo.is_published = True
        courseinfo.save()
        return Response({"msg": "Published Course"}, status.HTTP_200_OK)

    @link(permission_classes=((IsOwner, )))
    def approved_students(self, request, pk=None):
        """
            List approved students in the course
        """
        _course = get_object_or_404(Course, pk=pk)
        if (_course.type == 'T'):
            return Response({'response': False, 'students': []})
        self.check_object_permissions(request, _course)
        students = CourseHistory.objects.filter(course=_course, active='A')
        returned_data = []
        for student in students:
            user = User.objects.get(pk=student.user.id)
            returned_data.append({
                "user": user.id,
                "username": user.username,
                "fullname": user.get_full_name(),
                "email": user.email
            })
        return Response({'response': True, 'students': returned_data})

    @link(permission_classes=((IsOwner, )))
    def pending_students(self, request, pk=None):
        """
            List the students which are pending approval in the course
        """
        _course = get_object_or_404(Course, pk=pk)
        if (_course.type == 'T'):
            return Response({'response': False, 'students': []})
        self.check_object_permissions(request, _course)
        students = CourseHistory.objects.filter(course=_course, active='P')
        returned_data = []
        for student in students:
            user = User.objects.get(pk=student.user.id)
            returned_data.append({
                "user": user.id,
                "username": user.username,
                "fullname": user.get_full_name(),
                "email": user.email,
            })
        return Response({'response': True, 'students': returned_data})

    @action(methods=['POST'], permission_classes=((IsOwner, )))
    def approve(self, request, pk=None):
        """
            This function takes a list of student ids and
            approve their request to register
        """
        _course = get_object_or_404(Course, pk=pk, type='O')
        self.check_object_permissions(request, _course)
        if 'students' in request.DATA:
            # converting a string representation of array to
            students = ast.literal_eval(request.DATA['students'])
            for student in students:
                try:
                    coursehistory = CourseHistory.objects.get(
                        course=_course,
                        user=student,
                        active='P'
                    )
                    coursehistory.active = 'A'
                    coursehistory.save()
                except:
                    continue
            return Response({"msg": 'Success'}, status.HTTP_200_OK)
        else:
            print request.DATA
            return Response({"error": "Bad request format"}, status.HTTP_400_BAD_REQUEST)

    @link()
    def register(self, request, pk=None):
        """
            Register a student to a course.
        """
        course = get_object_or_404(Course, pk=pk, type='O')
        try:
            coursehistory = CourseHistory.objects.get(
                course=course,
                user=request.user,
            )
            if coursehistory.active == 'U':
                coursehistory.active = 'A'
                coursehistory.save()
                #  TODO: shift the usersetting to the approve function
                usersetting = UserSetting.objects.filter(
                    user=request.user, forum=course.forum)
                if len(usersetting) > 0:
                    usersetting = usersetting[0]
                    usersetting.is_active = True
                    usersetting.save()
                return Response("Successfully registered", status.HTTP_202_ACCEPTED)
            else:
                return Response(
                    "Your approval is pending. Please contact instructor for your approval",
                    status.HTTP_400_BAD_REQUEST
                )
        except:
            coursehistory = CourseHistory(
                course=course,
                user=request.user,
                active='A'
            )
            if course.enrollment_type == 'M':
                coursehistory.active = 'P'
            coursehistory.save()
            usersetting = UserSetting(user=request.user, forum=course.forum)
            usersetting.save()
            return Response("Successfully registered", status.HTTP_202_ACCEPTED)

    # TODO : should be action and not link
    # TODO : register and deregister should be sent to OfferingViewSet
    # TODO : user active should also be made choice field
    @link()
    def deregister(self, request, pk=None):
        course = get_object_or_404(Course, pk=pk, type='O')
        try:
            coursehistory = CourseHistory.objects.get(
                course=course,
                user=request.user,
                # an owner cannot deregister himself from the course
                is_owner=False
            )
            if coursehistory.active != 'U':
                coursehistory.active = 'U'
                coursehistory.save()
                usersetting = UserSetting.objects.filter(
                    user=request.user, forum=course.forum)
                if len(usersetting) > 0:
                    usersetting = usersetting[0]
                    usersetting.is_active = False
                    usersetting.save()
            return Response(CourseSerializer(course).data)
        except:
            error = 'You were not registered in this course.'
            return Response(error)

    @link(permission_classes=((IsRegistered, )))
    def progress(self, request, pk=None):
        """
        Function to get marks in a course
        """
        _course = get_object_or_404(Course, pk=pk)
        self.check_object_permissions(request, _course)
        history = get_object_or_404(
            CourseHistory,
            course=_course,
            user=request.user
        )
        return Response(history.progress())

    @link(permission_classes=((IsRegistered,)))
    def get_all_public_marks(self, request, pk=None):
        """
            Function to get marks of all the students for whom show_marks is true
        """
        _course = get_object_or_404(Course, pk=pk)
        self.check_object_permissions(request, _course)
        histories = CourseHistory.objects.filter(
            course=_course, is_owner=False, show_marks=True).order_by('score').reverse()
        data = {}
        data['students'] = []
        i = 0
        for history in histories:
            data['students'].append({})
            data['students'][i]['score'] = history.score
            data['students'][i]['max_score'] = history.course.max_score
            data['students'][i]['user'] = history.user.username
            data['students'][i]['id'] = history.user.id
            data['students'][i]['name'] = history.user.get_full_name()
            i += 1
        return Response(data)

    @link(permission_classes=((IsRegistered,)))
    def get_all_public_marks_student(self, request, pk=None):
        """
            Function to get marks of a student for whom show_marks is true
        """
        _course = get_object_or_404(Course, pk=pk)
        studentID = self.request.QUERY_PARAMS.get('student', None)
        _student = get_object_or_404(User, pk=studentID)
        self.check_object_permissions(request, _course)
        history = CourseHistory.objects.get(
            course=_course, user=_student, is_owner=False, show_marks=True)
        data = {}
        data = (history.progress())
        data['user'] = history.user.username
        data['id'] = history.user.id
        data['name'] = history.user.get_full_name()
        return Response(data)

    @link(permission_classes=((IsOwner,)))
    def get_all_marks(self, request, pk=None):
        """
            Function to get marks of all the students
        """
        _course = get_object_or_404(Course, pk=pk)
        self.check_object_permissions(request, _course)
        histories = CourseHistory.objects.filter(
            course=_course, is_owner=False).order_by('score').reverse()
        data = {}
        data['students'] = []
        i = 0
        for history in histories:
            data['students'].append({})
            data['students'][i]['score'] = history.score
            data['students'][i]['max_score'] = history.course.max_score
            data['students'][i]['user'] = history.user.username
            data['students'][i]['id'] = history.user.id
            data['students'][i]['name'] = history.user.get_full_name()
            i += 1
        return Response(data)

    @link(permission_classes=((IsOwner,)))
    def get_all_marks_student(self, request, pk=None):
        """
            Function to get marks of a student
        """
        _course = get_object_or_404(Course, pk=pk)
        studentID = self.request.QUERY_PARAMS.get('student', None)
        _student = get_object_or_404(User, pk=studentID)
        self.check_object_permissions(request, _course)
        history = CourseHistory.objects.get(
            course=_course, user=_student, is_owner=False)

        data = {}
        data = (history.progress())
        data['user'] = history.user.username
        data['id'] = history.user.id
        data['name'] = history.user.get_full_name()
        return Response(data)

    @link(permission_classes=((IsOwnerOrReadOnly, )))
    def groups(self, request, pk=None):
        """
        Function to get all the groups in a course
        """
        _course = get_object_or_404(Course, pk=pk)
        self.check_object_permissions(request, _course)
        _groups = Group.objects.filter(course=_course)
        serializer = GroupSerializer(_groups, many=True)
        _playlist = playlist.to_array(_course.playlist)
        N = len(_playlist)
        ordered_data = [""] * N
        for i in range(N):
            ordered_data[i] = serializer.data[_playlist[i][1]]
        return Response(ordered_data)

    @action(
        methods=['POST'],
        permission_classes=((IsOwnerOrReadOnly,)),
        serializer_class=AddGroupSerializer)
    def add_group(self, request, pk=None):
        _course = get_object_or_404(Course, pk=pk)
        self.check_object_permissions(request, _course)
        serializer = AddGroupSerializer(data=request.DATA)
        if serializer.is_valid():
            if request.FILES == {}:
                group = Group(
                    course=_course,
                    title=serializer.data['title'],
                    description=serializer.data['description']
                )
            else:
                group = Group(
                    course=_course,
                    title=serializer.data['title'],
                    description=serializer.data['description'],
                    image=request.FILES['image']
                )
            group.save()
            _course.playlist = playlist.append(group.id, _course.playlist)
            _course.save()
            return Response(GroupSerializer(group).data)
        else:
            content = serializer.errors
            return Response(content, status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['PATCH'],
        permission_classes=((IsOwnerOrReadOnly,)),
        serializer_class=CourseSerializer)
    def reorder_groups(self, request, pk=None):
        _course = get_object_or_404(Course, pk=pk)
        self.check_object_permissions(request, _course)
        myplaylist = request.DATA['playlist']
        newplaylist = playlist.is_valid(myplaylist, _course.playlist)
        if newplaylist is not False:
            _course.playlist = newplaylist
            _course.save()
            return Response(_course.playlist)
        else:
            content = "Given order data does not have the correct format"
            return Response(content, status.HTTP_404_NOT_FOUND)

    @action(methods=['PATCH'], permission_classes=((IsRegistered,)))
    def set_marks_setting(self, request, pk=None):
        _course = get_object_or_404(Course, pk=pk)
        history = CourseHistory.objects.get(
            course=_course, user=self.request.user)
        show_marks = self.request.QUERY_PARAMS.get('show', None)
        if(show_marks == 'true'):
            history.show_marks = True
        else:
            history.show_marks = False
        history.save()
        return Response(history.show_marks)

    @link(permission_classes=((IsRegistered,)))
    def get_marks_setting(self, request, pk=None):
        _course = get_object_or_404(Course, pk=pk)
        history = CourseHistory.objects.get(
            course=_course, user=self.request.user)
        return Response(history.show_marks)


class OfferingViewSet(viewsets.ModelViewSet):

    """
    ViewSet for model Offering
    """
    model = Offering
    serializer_class = OfferingSerializer
    permission_classes = [IsInstructorOrReadOnly]

    def get_queryset(self):
        """
        Optionally restricts the returned courses to a given category.
        """
        queryset = Offering.objects.all()
        category = self.request.QUERY_PARAMS.get('category', None)
        if category is not None:
            queryset = queryset.filter(category__id=category)
        return queryset

    def create(self, request, pk=None, *args):
        """
        Function for creating an offering in a category
        """
        serializer = OfferingSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            coursehistory = CourseHistory(
                user=request.user,
                course=serializer.object,
                active='A',
                is_owner=True
            )
            coursehistory.save()

            # Usersetting for the discussion forum
            usersetting = UserSetting(
                user=request.user,
                forum=serializer.object.forum, super_user=True, moderator=True, badge='IN')
            usersetting.save()
            # send for approval now

            ## Create a 'General' tag for each course
            tag = Tag(forum=serializer.object.forum)
            tag.tag_name = 'General'
            tag.title = 'General'
            tag.save()

            return Response(serializer.data)
        else:
            content = serializer.errors
            return Response(content, status.HTTP_400_BAD_REQUEST)

    @link(permission_classes=((IsOwner, )))
    def get_shortlisted_courses(self, request, pk=None):
        mycourse = get_object_or_404(Offering, pk=pk)
        self.check_object_permissions(request, mycourse)
        shortlist = mycourse.shortlisted_courses.all()
        serializer = CourseSerializer(shortlist, many=True)
        return Response(serializer.data)

    @action(methods=['POST'], permission_classes=((IsOwner, )))
    def shortlist_course(self, request, pk=None):
        mycourse = get_object_or_404(Offering, pk=pk)
        self.check_object_permissions(request, mycourse)
        try:
            _course = Course.objects.get(pk=request.DATA['id'], type='T')
        except:
            return Response("Bad Request: No such textbook", status.HTTP_400_BAD_REQUEST)

        mycourse.shortlisted_courses.add(_course)
        return Response("Successfully shortlisted the course", status.HTTP_202_ACCEPTED)


class CourseHistoryViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):

    """
    ViewSet for CourseHistory. Only gives Update option
    """
    model = CourseHistory
    serializer_class = CourseHistorySerializer
    permission_classes = [IsInstructorOrReadOnly]

    @link(permission_classes=((IsRegistered, )))
    def concept_history(self, request, pk=None):
        coursehistory = get_object_or_404(CourseHistory, pk=pk)
        self.check_object_permissions(request, coursehistory.course)
        history = ConceptHistory.objects.filter(
            user=request.user, course_history=coursehistory)
        serializer = ConceptHistorySerializer(history, many=True)
        return Response(serializer.data)


class CourseInfoViewSet(viewsets.ModelViewSet):
    queryset = CourseInfo.objects.all()
    serializer_class = CourseInfoSerializer
