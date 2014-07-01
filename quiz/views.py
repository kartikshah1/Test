"""
Views for the Quiz API
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from rest_framework import mixins, status, viewsets
from rest_framework.decorators import link, action
from rest_framework.response import Response

from quiz.grader import Grader
from quiz.models import QuestionModule, Question, FixedAnswerQuestion, \
    Submission, Quiz, QuestionHistory, SingleChoiceQuestion, \
    MultipleChoiceQuestion
from quiz import serializers
from quiz import permissions
from courseware import playlist


@login_required
def view(request):
    """ Normal view """
    return render(request, 'quiz/quiz.html', {})


@login_required
def admin(request):
    """ Admin view """
    return render(request, 'quiz/quiz_admin.html', {})


class QuizViewSet(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  # TODO: remove LIST when course API is complete
                  mixins.DestroyModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """
    QuizViewSet:
    - get_question_modules
    - add_question_module
    - get_questions_manual_grade
    """

    model = Quiz
    serializer_class = serializers.QuizSerializer
    permission_classes = [permissions.IsCourseInstructor]
    paginate_by = None

    def destroy(self, request, pk=None):
        quiz = get_object_or_404(Quiz, pk=pk)
        # concept removed from quiz object
        # concept = quiz.concept
        # concept.quiz_playlist = playlist.delete(concept.quiz_playlist, pk=pk)
        # concept.save()
        return super(QuizViewSet, self).destroy(request, pk)

    @link(permission_classes=(permissions.IsEnrolled,))
    def get_question_modules(self, request, pk=None):
        """
        Return list of question modules
        """
        quiz = get_object_or_404(Quiz, pk=pk)
        self.check_object_permissions(request, quiz)
        question_modules = QuestionModule.objects.filter(quiz=quiz)
        serializer = serializers.QuestionModuleSerializer(question_modules,
                                                          many=True)
        return Response(serializer.data)

    @action(permission_classes=(permissions.IsCourseInstructor,))
    def add_question_module(self, request, pk=None):
        """
        Add a question module
        """
        quiz = get_object_or_404(Quiz, pk=pk)
        self.check_object_permissions(request, quiz)
        serializer = serializers.QuestionModuleSerializer(data=request.DATA)
        if serializer.is_valid():
            question_module = QuestionModule(
                quiz=quiz,
                title=serializer.data['title'],
                dummy=serializer.data['dummy'],
            )
            question_module.save()

            serializer = serializers.QuestionModuleSerializer(question_module)
            return Response(serializer.data)
        else:
            content = serializer.errors
            return Response(content, status.HTTP_400_BAD_REQUEST)

    @link(permission_classes=(permissions.IsCourseInstructor,))
    def get_questions_manual_grade(self, request, pk=None):
        """
        Return the list of questions which have to manually graded
        """
        quiz = get_object_or_404(Quiz, pk=pk)
        self.check_object_permissions(request, quiz)
        questions = Question.objects.filter(
            quiz=quiz,
            grader_type=Question.MANUAL_GRADING
        )
        serializer = serializers.QuestionSerializer(questions, many=True)
        return Response(serializer.data)


class QuestionModuleViewSet(mixins.DestroyModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            viewsets.GenericViewSet):
    """
    QuestionModuleViewSet:
    - get_questions
    - add_fixed_answer_question
    - add_single_choice_question
    """
    model = QuestionModule
    serializer_class = serializers.QuestionModuleSerializer
    permission_classes = [permissions.IsCourseInstructor]
    paginate_by = None

    def get_question_and_history_data(self, question, question_history):
        """
        Get a dict of user history of a question and question data
        This function is meant for showing to user and not admin
        """
        hint = None
        if question_history.hint_taken:
            hint = question.hint
        answer = None
        answer_description = None
        question = Question.objects.get_subclass(pk=question.pk)
        if question_history.answer_shown:
            answer = question.get_answer(showToUser=True)
            if question.answer_description == '':
                answer_description = None
            else:
                answer_description = question.answer_description
        data = {
            'id': question.pk,
            'marks': question.marks,
            'attempts': question.attempts,
            'description': question.description,
            'is_hint_available': question.is_hint_available(),
            'type': question.type,
            'user_attempts': question_history.attempts,
            'user_marks': question_history.marks,
            'user_status': question_history.status,
            'hint_taken': question_history.hint_taken,
            'hint': hint,
            'answer_shown': question_history.answer_shown,
            'answer': answer,
            'answer_description': answer_description
        }

        if question.type == question.FIXED_ANSWER_QUESTION:
            pass
        elif question.type == question.SINGLE_CHOICE_QUESTION:
            data['options'] = question.options
            # print "detected single choice question", data
        elif question.type == question.MULTIPLE_CHOICE_QUESTION:
            data['options'] = question.options
        return data

    @link(permission_classes=(permissions.IsCourseInstructor,))
    def get_questions_admin(self, request, pk=None):
        """
        Return list of questions
        """
        question_module = get_object_or_404(QuestionModule, pk=pk)
        self.check_object_permissions(request, question_module)
        questions = Question.objects.filter(question_module=question_module)
        serializer = serializers.AdminQuestionSerializer(questions, many=True)
        data = serializer.data
        new_data = []
        for question in data:
            the_question = Question.objects.get_subclass(pk=question['id'])
            answer_fields = the_question.get_answer_data()
            question['answer_fields'] = answer_fields
            new_data.append(question)
        return Response(new_data, status.HTTP_200_OK)

    @link(permission_classes=(permissions.IsEnrolled,))
    def get_questions(self, request, pk=None):
        """
        Return list of questions
        """
        question_module = get_object_or_404(QuestionModule, pk=pk)
        self.check_object_permissions(request, question_module)
        questions = Question.objects.filter(question_module=question_module)
        data = []
        for question in questions:
            # print "found question ", question
            question_history, created = QuestionHistory.objects.get_or_create(
                question=question,
                student=request.user
            )
            question_history.save()
            data.append(self.get_question_and_history_data(
                question, question_history))
        serializer = serializers.FrontEndQuestionSerializer(data, many=True)
        return Response(serializer.data)

    @action(permission_classes=(permissions.IsCourseInstructor,))
    def add_fixed_answer_question(self, request, pk=None):
        """
        Add a fixed answer question
        """
        question_module = get_object_or_404(QuestionModule, pk=pk)
        self.check_object_permissions(request, question_module)
        serializer = serializers.FixedAnswerQuestionSerializer(
            data=request.DATA)
        # Figure out a better way to set None values and modify incoming data
        if serializer.is_valid():
            serializer.data['question_module'] = question_module
            serializer.data['quiz'] = question_module.quiz
            question = FixedAnswerQuestion(**serializer.data)
            question.save()
            serializer = serializers.FixedAnswerQuestionSerializer(question)
            return Response(serializer.data)
        else:
            content = serializer.errors
            return Response(content, status.HTTP_400_BAD_REQUEST)

    @action(permission_classes=(permissions.IsCourseInstructor,))
    def add_single_choice_question(self, request, pk=None):
        """
        Add a single choice correct Question
        """
        question_module = get_object_or_404(QuestionModule, pk=pk)
        self.check_object_permissions(request, question_module)
        serializer = serializers.SingleChoiceQuestionSerializer(
            data=request.DATA)
        if serializer.is_valid():
            serializer.data['question_module'] = question_module
            serializer.data['quiz'] = question_module.quiz
            question = SingleChoiceQuestion(**serializer.data)
            question.save()
            serializer = serializers.SingleChoiceQuestionSerializer(question)
            return Response(serializer.data)
        else:
            content = serializer.errors
            return Response(content, status.HTTP_400_BAD_REQUEST)

    @action(permission_classes=(permissions.IsCourseInstructor,))
    def add_multiple_choice_question(self, request, pk=None):
        """
        Add a multiple choice correct Question
        """
        question_module = get_object_or_404(QuestionModule, pk=pk)
        self.check_object_permissions(request, question_module)
        serializer = serializers.MultipleChoiceQuestionSerializer(
            data=request.DATA)
        if serializer.is_valid():
            serializer.data['question_module'] = question_module
            serializer.data['quiz'] = question_module.quiz
            question = MultipleChoiceQuestion(**serializer.data)
            question.save()
            serializer = serializers.MultipleChoiceQuestionSerializer(question)
            return Response(serializer.data)
        else:
            content = serializer.errors
            return Response(content, status.HTTP_400_BAD_REQUEST)


class FixedAnswerQuestionViewSet(mixins.RetrieveModelMixin,
                                 mixins.UpdateModelMixin,
                                 viewsets.GenericViewSet):
    """
    FixedAnswerQuestionViewSet:
    """

    model = FixedAnswerQuestion
    serializer_class = serializers.FixedAnswerQuestionSerializer
    permission_classes = [permissions.IsCourseInstructor]
    paginate_by = None


class SingleChoiceQuestionViewSet(mixins.RetrieveModelMixin,
                                  mixins.UpdateModelMixin,
                                  viewsets.GenericViewSet):
    """
    SingleChoiceQuestionViewSet:
    """

    model = SingleChoiceQuestion
    serializer_class = serializers.SingleChoiceQuestionSerializer
    permission_classes = [permissions.IsCourseInstructor]
    paginate_by = None


class MultipleChoiceQuestionViewSet(mixins.CreateModelMixin,
                                    # TODO: remove CREATE when add_quiz is added to concept
                                    # TODO: remove LIST when course API is complete
                                    mixins.ListModelMixin,
                                    mixins.DestroyModelMixin,
                                    mixins.RetrieveModelMixin,
                                    mixins.UpdateModelMixin,
                                    viewsets.GenericViewSet):
    """
    SingleChoiceQuestionViewSet:
    """

    model = MultipleChoiceQuestion
    serializer_class = serializers.MultipleChoiceQuestionSerializer
    permission_classes = [permissions.IsCourseInstructor]
    paginate_by = None


class QuestionViewSet(mixins.DestroyModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      viewsets.GenericViewSet):
    """
    QuestionViewSet:
    - get_hint
    - get_answer
    - submit_answer
    - get_submissions_manual_grade
    """

    model = Question
    serializer_class = serializers.AdminQuestionSerializer
    permission_classes = [permissions.IsCourseInstructor]
    paginate_by = None

    @link(permission_classes=(permissions.IsEnrolled,))
    def get_hint(self, request, pk=None):
        """
        Return the answers to the questions
        """
        question = get_object_or_404(Question, pk=pk)
        self.check_object_permissions(request, question)
        hint = {
            'id': question.pk,
            'hint': question.hint
        }
        try:
            question_history = QuestionHistory.objects.get(
                student=request.user,
                question=question
            )
            question_history.hint_taken = True
            question_history.save()
        except:
            error = {
                'status': False,
                'detail': 'Question History not found'
            }
            return Response(error, status.HTTP_400_BAD_REQUEST)
        return Response(hint)

    @link(permission_classes=(permissions.IsEnrolled,))
    def get_answer(self, request, pk=None):
        """
        Return the answers to the questions
        """
        # Currently no UI uses this view
        question = get_object_or_404(Question, pk=pk)
        self.check_object_permissions(request, question)
        try:
            question_history = QuestionHistory.objects.get(
                student=request.user,
                question=question
            )
            if question_history.attempts < question.attempts:
                remaining = question.attempts - question_history.attempts
                error = {
                    'status': False,
                    'detail': str(remaining) + ' attempts still remaining'
                }
                return Response(error, status.HTTP_400_BAD_REQUEST)
            if question_history.status == QuestionHistory.AWAITING_RESULTS:
                error = {
                    'status': False,
                    'detail': 'Please wait for some time'
                }
                return Response(error, status.HTTP_400_BAD_REQUEST)
            if question_history.status != QuestionHistory.SOLVED:
                error = {
                    'status': False,
                    'detail': 'You have not solved the question yet'
                }
                return Response(error, status.HTTP_400_BAD_REQUEST)
            question_history.answer_shown = True
            question_history.save()
        except:
            error = {
                'detail': 'Internal error 3001'
            }
            return Response(error)
        que = Question.objects.get_subclass(pk=question.pk)
        answer = {
            'id': que.pk,
            'status': True,
            'answer_description': que.answer_description,
            'answer': que.get_answer(showToUser=True),
        }
        return Response(answer)

    @action(permission_classes=(permissions.IsEnrolled,))
    def submit_answer(self, request, pk=None):
        """ Submit an answer to a question """
        print "submit_answer : ", request
        question = get_object_or_404(Question, pk=pk)
        self.check_object_permissions(request, question)

        question_history = QuestionHistory.objects.get(
            student=request.user,
            question=question
        )

        if question_history.status == QuestionHistory.AWAITING_RESULTS:
            error = {
                'status': False,
                'detail': 'Please wait for some time'
            }
            return Response(error, status.HTTP_400_BAD_REQUEST)

        if question_history.status == QuestionHistory.SOLVED:
            error = {
                'status': False,
                'detail': 'Question already answered'
            }
            return Response(error, status.HTTP_400_BAD_REQUEST)

        if question_history.answer_shown:
            error = {
                'status': False,
                'detail': 'Question already attempted',
            }
            return Response(error, status.HTTP_400_BAD_REQUEST)

        if question_history.attempts >= question.attempts:
            error = {
                'status': False,
                'detail': 'Exceeded the maximum number of attempts'
            }
            return Response(error, status.HTTP_400_BAD_REQUEST)

        question_history.attempts += 1
        attempts_remaining = question.attempts - question_history.attempts

        serializer = serializers.AnswerSubmitSerializer(data=request.DATA)
        if serializer.is_valid():
            # Evaluate the submission and put in the submission
            question_history.status = QuestionHistory.AWAITING_RESULTS

            submission = Submission(
                #course=question.course,
                question=question,
                student=request.user,
                grader_type=question.grader_type,
                answer=serializer.data['answer']
            )
            # Optimization: let the grader save the submission
            # submission.save()
            data = {
                'status': submission.status,
                'is_correct': submission.is_correct,
                'result': submission.result,
                'attempts_remaining': attempts_remaining
            }

            grader = Grader(submission=submission,
                            question=question,
                            question_history=question_history)
            if grader.grade():
                submission = grader.submission
                data['status'] = submission.status
                data['is_correct'] = submission.is_correct
                data['result'] = submission.result
                if attempts_remaining == 0 or submission.is_correct:
                    if grader.the_question is None:
                        the_question = Question.objects.get_subclass(
                            pk=submission.question.pk)
                        data['answer'] = \
                            the_question.get_answer(showToUser=True)
                    else:
                        data['answer'] = \
                            grader.the_question.get_answer(showToUser=True)
                    data['answer_description'] = question.answer_description
                serializer = serializers.FrontEndSubmissionSerializer(data)
            else:
                serializer = serializers.FrontEndSubmissionSerializer(data)

            # return the result of grading
            return Response(serializer.data)
        else:
            question_history.save()
            content = serializer.errors
            return Response(content, status.HTTP_400_BAD_REQUEST)

    @link(permission_classes=(permissions.IsCourseInstructor,))
    def get_submissions_manual_grade(self, request, pk=None):
        """
        Return the list of submissions which have to manually graded
        """
        question = get_object_or_404(Question, pk=pk)
        self.check_object_permissions(request, question)
        submissions = Submission.objects.filter(question=question)
        serializer = serializers.SubmissionSerializer(submissions, many=True)
        return Response(serializer.data)


class SubmissionViewSet(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):
    """
    SubmissionViewSet:
    - set_plagiarised
    """
    model = Submission
    serializer_class = serializers.SubmissionSerializer
    permission_classes = [permissions.IsCourseInstructor]
    paginate_by = None

    @action(permission_classes=(permissions.IsCourseInstructor,))
    def set_plagiarised(self, request, pk=None):
        """
        Set the submission to be plagiarised
        """
        serializer = serializers.PlagiarismSerializer(data=request.DATA)
        if serializer.is_valid():
            submission = get_object_or_404(Submission, pk=pk)
            self.check_object_permissions(request, submission)
            submission.is_plagiarised = serializer.data['is_plagiarised']
            submission.has_been_checked = True
            submission.save()
            return Response(serializers.SubmissionSerializer(submission).data)
        else:
            content = serializer.errors
            return Response(content, status.HTTP_400_BAD_REQUEST)
