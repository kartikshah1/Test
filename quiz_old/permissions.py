""""
Handles permission for Quiz API

Permission Classes:
    IsEnrolled
    - Any course instructor or student of the course had the permission to
      fetch the quiz

    IsCourseInstructor
    - the course instructors have full access to adding, deleting, editing a
      quiz and its questions

Quiz
    + create: IsCourseInstructor
    + destroy: IsCourseInstructor
    + retrieve: IsEnrolled
    + update: IsCourseInstructor
    - get_question_modules: IsEnrolled
    - add_question_module: IsCourseInstructor
    - get_questions_manual_grade: IsCourseInstructor

QuestionModule
    + destroy: IsCourseInstructor
    + retrieve: IsEnrolled
    + update: IsCourseInstructor
    - get_questions: IsEnrolled
    - add_fixed_answer_question: IsCourseInstructor

FixedAnswerQuestion
    + destroy: IsCourseInstructor
    + retrieve: IsEnrolled
    + update: IsCourseInstructor

Question
    + retrieve: IsEnrolled
    + update: IsCourseInstructor
    - get_answer: IsCourseInstructorOrMaxAttempted
    - submit_answer: IsEnrolled
    - get_submissions_manual_grade: IsCourseInstructor

Submission
    + retrieve: IsEnrolled
    + update: IsCourseInstructor
    - set_plagiarised: IsCourseInstructor
"""

from rest_framework import permissions

from courseware import models
from quiz import models


class IsEnrolled(permissions.BasePermission):
    """
    Allows view permission to anyone enrolled
    """

    def has_permission(self, request, view):
        """
        Allow loggedIn users only
        """
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        """
        Returns whether user has permission on this object or not
        """
        return True
        if not request.user.is_authenticated():
            return False
        try:
            #course = obj.course
            course = models.Course.objects.get(pk=1)
            course_history = models.CourseHistory.objects.get(
                course=course,
                user=request.user)
            return True
        except:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return False


class IsCourseInstructor(permissions.BasePermission):
    """
    Allows complete permission to course instructor
    """

    def has_permission(self, request, view):
        """
        Allow loggedIn users only
        """
        return request.user.is_authenticated()

    def has_object_permission(self, request, view, obj):
        """
        Returns whether user has permission on this object or not
        """
        return True
        if not request.user.is_authenticated():
            return False
        try:
            #course = obj.course
            course = models.Course.objects.get(pk=1)
            course_history = models.CourseHistory.objects.get(
                course=course,
                user=request.user)
            if course_history.is_instructor:
                return True
            else:
                return False
        except:
            return False
