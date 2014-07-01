"""
Views for Quiz_Template
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from rest_framework import mixins, status, viewsets
from rest_framework.decorators import link, action
from rest_framework.response import Response

from quiz_template.models import Quiz, Question_Module, Question_Master,\
    Question_Mcq, Question_Scq, Question_Fix, Question_Des, User_Submissions
from quiz_template import serializers
from grader import Grader


def view(request):
    """ Normal view """
    return render(request, 'quiz_template/quiz.html', {})


class QuizViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):

    """
    QuizViewSet
    """
    model = Quiz
    serializer_class = serializers.QuizSerializer
    paginate_by = None

    @link()
    def get_question_modules(self, request, pk=None):
        """
        Return list of question modules
        """
        quiz = get_object_or_404(Quiz, pk=pk)
        self.check_object_permissions(request, quiz)
        question_modules = Question_Module.objects.filter(quiz=quiz)
        serializer = serializers.QuestionModuleSerializer(question_modules,
                                                          many=True)
        return Response(serializer.data)


class QuestionModuleViewSet(mixins.CreateModelMixin,
                            mixins.DestroyModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            viewsets.GenericViewSet):

    """
    QuestionModuleViewSet
    """
    model = Question_Module
    serializer_class = serializers.QuestionModuleSerializer
    paginate_by = None

    def get_question_and_submission_data(self, question, submission):
        """
        Get a dict of user history of a question and question data
        This function is meant for showing to user and not admin
        """
        hint = None
        if submission.hint_taken:
            hint = question.hint
        answer = None
        question = Question_Master.objects.get_subclass(pk=question.pk)
        if submission.is_answer_shown():
            answer = question.get_answer()

        data = {
            'id': question.pk,
            'marks': question.get_max_marks(),
            'attempts': question.attempts,
            'text': question.text,
            'is_hint_available': question.is_hint_available(),
            'type': question.type,
            'user_attempts': submission.attempts,
            'user_marks': submission.marks,
            'user_status': submission.status,
            'hint_taken': submission.hint_taken,
            'hint': hint,
            'answer_shown': submission.is_answer_shown(),
            'answer': answer,
            'explaination': submission.explaination
        }

        if question.type == question.SINGLE_CHOICE_QUESTION:
            data['options'] = question.options
        elif question.type == question.MULTIPLE_CHOICE_QUESTION:
            data['options'] = question.options
        return data

    @link()
    def get_questions(self, request, pk=None):
        """
        Return list of questions
        """
        question_module = get_object_or_404(Question_Module, pk=pk)
        self.check_object_permissions(request, question_module)
        questions = Question_Master.objects.filter(module=question_module)
        data = []
        for question in questions:
            # print "found question ", question
            user_submissions, created = User_Submissions.objects.get_or_create(
                question=question,
                user=request.user
            )
            user_submissions.save()
            data.append(self.get_question_and_submission_data(
                question, user_submissions))
        serializer = serializers.FrontEndQuestionSerializer(data, many=True)
        return Response(serializer.data)


class QuestionMasterViewSet(mixins.CreateModelMixin,
                            mixins.DestroyModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            viewsets.GenericViewSet):

    """
    QuestionMasterViewSet
    """
    model = Question_Master
    serializer_class = serializers.QuestionMasterSerializer
    paginate_by = None

    @link()
    def get_hint(self, request, pk=None):
        """
        Return the hint to the questions
        """
        question = get_object_or_404(Question_Master, pk=pk)
        self.check_object_permissions(request, question)
        hint = {
            'id': question.pk,
            'hint': question.hint
        }
        try:
            submission = User_Submissions.objects.get(
                user=request.user,
                question=question
            )
            submission.hint_taken = True
            submission.save()
        except:
            error = {
                'status': False,
                'detail': 'Submission not found'
            }
            return Response(error, status.HTTP_400_BAD_REQUEST)
        return Response(hint)

    @action()
    def submit_answer(self, request, pk=None):
        """Submit an answer to a question"""
        question = get_object_or_404(Question_Master, pk=pk)
        self.check_object_permissions(request, question)

        submission = User_Submissions.objects.get(
            user=request.user,
            question=question
        )

        if submission.status == submission.CORRECT or submission.status == submission.WRONG:
            error = {
                'status': False,
                'detail': 'Question already answered'
            }
            return Response(error, status.HTTP_400_BAD_REQUEST)

        if submission.is_answer_shown():
            error = {
                'status': False,
                'detail': 'Question already attempted',
            }
            return Response(error, status.HTTP_400_BAD_REQUEST)

        if submission.attempts >= question.attempts:
            error = {
                'status': False,
                'detail': 'Exceeded the maximum number of attempts'
            }
            return Response(error, status.HTTP_400_BAD_REQUEST)

        submission.attempts += 1
        attempts_remaining = question.attempts - submission.attempts

        serializer = serializers.AnswerSubmitSerializer(data=request.DATA)
        print serializer
        if serializer.is_valid():
            submission.status = User_Submissions.ATTEMPTED
            submission.answer = serializer.data['answer']

            data = {
                'status': submission.status,
                'marks': submission.marks,
                'attempts_remaining': attempts_remaining,
                'explaination': submission.explaination
            }

            grader = Grader(submission=submission, question=question)
            if grader.grade():
                submission = grader.submission
                data['status'] = submission.status
                data['marks'] = submission.marks
                data['explaination'] = submission.explaination
                if attempts_remaining == 0 or submission.status == User_Submissions.CORRECT:
                    if grader.the_question is None:
                        the_question = Question.objects.get_subclass(
                            pk=submission.question.pk)
                        data['answer'] = \
                            the_question.get_answer()
                    else:
                        data['answer'] = \
                            grader.the_question.get_answer()
                serializer = serializers.FrontEndSubmissionSerializer(data)
            else:
                serializer = serializers.FrontEndSubmissionSerializer(data)

            # return the result of grading
            return Response(serializer.data)
        else:
            submission.save()
            content = serializer.errors
            return Response(content, status.HTTP_400_BAD_REQUEST)


class QuestionScqViewSet(mixins.CreateModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         viewsets.GenericViewSet):

    """
    QuestionScqViewSet
    """
    model = Question_Scq
    serializer_class = serializers.QuestionScqSerializer
    paginate_by = None


class QuestionMcqViewSet(mixins.CreateModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         viewsets.GenericViewSet):

    """
    QuestionMcqViewSet
    """
    model = Question_Mcq
    serializer_class = serializers.QuestionMcqSerializer
    paginate_by = None


class QuestionFixViewSet(mixins.CreateModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         viewsets.GenericViewSet):

    """
    QuestionFixViewSet
    """
    model = Question_Fix
    serializer_class = serializers.QuestionFixSerializer
    paginate_by = None


class QuestionDesViewSet(mixins.CreateModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         viewsets.GenericViewSet):

    """
    QuestionDesViewSet
    """
    model = Question_Des
    serializer_class = serializers.QuestionDesSerializer
    paginate_by = None


class UserSubmissionsViewSet(mixins.CreateModelMixin,
                             mixins.DestroyModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             viewsets.GenericViewSet):

    """
    QuestionModuleViewSet
    """
    model = User_Submissions
    serializer_class = serializers.UserSubmissionsSerializer
    paginate_by = None
