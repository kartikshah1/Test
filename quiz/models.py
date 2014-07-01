"""
This file contains models for the Quiz module of the e-learning platform
It has models defined for the Quiz, QuestionModule, Question and Submissions
Also defines the model for saving the history for the above
"""

import json
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch.dispatcher import receiver

from util.models import HitCounter, TimeKeeper
from util.methods import receiver_subclasses
from model_utils.managers import InheritanceManager

import courseware


class Quiz(models.Model):
    """
    This class encapsulates the model of a quiz.
    """
    title = models.TextField()  # title of the quiz
    # Number of question modules in Quiz, Auto
    question_modules = models.IntegerField(default=0)
    # Number of questions in Quiz, Auto
    questions = models.IntegerField(default=0)
    marks = models.FloatField(default=0.0)  # max marks for this quiz
    # JSON Object used to maintain the order of question
    # modules in the Quiz
    playlist = models.TextField(default='[]')

    def update_score(self, difference):
        self.marks += difference
        self.save()
        try:
            concept = courseware.models.Concept.objects.get(quizzes__pk=self.id)
            concept.update_score(difference)
        except:
            return


class QuestionModule(models.Model):
    """
    Each quiz is composed of several QuestionModules where each QuestionModule
    can have 1 or more questions. When the Question Module contains
    only one question (thereby serving no purpose other than encapsulating
    the question), and you do not want to display/use the content of the
    module object itself, set the dummy flag to True
    """
    #course = models.ForeignKey(
    #    Course,
    #    related_name="QuestionModule_Course",
    #    db_index=True
    #)
    quiz = models.ForeignKey(Quiz, related_name='QuestionModule_Quiz')
    # title/description of the question module
    title = models.TextField()
    # Ordering of questions in the module
    playlist = models.TextField(default='[]')
    # Number of questions in Model, Auto
    questions = models.IntegerField(default=0)
    # flag whether the module is a dummy (for a single question)
    dummy = models.BooleanField(default=False)


class QuizHistory(models.Model):
    """
    This class captures the quiz history of a user
    """
    quiz = models.ForeignKey(Quiz, related_name='QuizHistory_Quiz')
    user = models.ForeignKey(User, related_name='QuizHistory_User')
    current_question_module = models.ForeignKey(
        QuestionModule, related_name='QuizHistory_QuestionModule', null=True)
    marks = models.FloatField(default=0.0)
    solved = models.IntegerField(default=0)  # Number of questions solved
    is_graded = models.BooleanField(default=False)

    def progress(self):
        data = {}
        data['title'] = self.quiz.title
        data['score'] = self.marks
        data['max_score'] = self.quiz.marks
        data['questions'] = self.quiz.questions
        data['solved'] = self.solved
        return data

    def update_score(self, difference):
        self.marks += difference
        self.save()
        try:
            concept = courseware.models.Concept.objects.get(quizzes__pk=self.quiz.id)
            ch, created = courseware.models.ConceptHistory.objects.get_or_create(
                concept=concept, user=self.user)
            ch.update_score(difference)
        except:
            return

    class Meta:
        """
        question and student combined should be unique
        """
        unique_together = ("quiz", "user")


class Question(HitCounter):
    """
    This is the basic gradable unit - a question. It can be of multiple types
    """

    MANUAL_GRADING = 'M'
    DIRECT_GRADING = 'D'
    GRADER_TYPES = (
        (MANUAL_GRADING, 'Manual Grading'),
        (DIRECT_GRADING, 'Direct Grading')
    )

    SINGLE_CHOICE_QUESTION = 'S'
    MULTIPLE_CHOICE_QUESTION = 'M'
    FIXED_ANSWER_QUESTION = 'F'
    DESCRIPTIVE_ANSWER_QUESTION = 'D'
    PROGRAMMING_QUESTION = 'P'
    QUESTION_TYPES = (
        (SINGLE_CHOICE_QUESTION, 'Single Choice Correct'),
        (MULTIPLE_CHOICE_QUESTION, 'Multiple Choice Correct'),
        (FIXED_ANSWER_QUESTION, 'Fixed Answer'),
        (DESCRIPTIVE_ANSWER_QUESTION, 'Descriptive Answer'),
        (PROGRAMMING_QUESTION, 'Programming Question')
    )

    #course = models.ForeignKey(
    #    Course,
    #    related_name="Question_Course",
    #    db_index=True
    #)
    quiz = models.ForeignKey(Quiz, related_name="Question_Quiz")
    question_module = models.ForeignKey(
        QuestionModule,
        related_name='Question_QuestionModule',
        db_index=True)  # index this field
    description = models.TextField()
    # hint_available = models.BooleanField(default=False)
    hint = models.TextField(
        help_text="Hint you want to give if any",
        blank=True,
        null=True)
    grader_type = models.CharField(
        max_length=1,
        help_text="Which grader to use for grading this question",
        choices=GRADER_TYPES,
        default='D')
    #order = models.IntegerField()
    answer_description = models.TextField(
        help_text="Description of the answer",
        blank=True)
    marks = models.FloatField(default=0)
    gradable = models.BooleanField(default=True)
    granularity = models.TextField(
        help_text="Enter a string with marks separated by commas. \
            Last entry will be repeated until infinity attempts")
    # granularity after the hint is given
    granularity_hint = models.TextField(
        help_text="Enter a string with marks separated by commas. \
        Last entry will be repeated until infinity attempts",
        blank=True,
        null=True)
    # type : this fields exists so that the question type can be accessed
    # directly. This need not be set explicitly. It is set automatically
    # in the child classes
    type = models.CharField(
        max_length=1,
        choices=QUESTION_TYPES,
        help_text="Type of question",
    )
    attempts = models.IntegerField(default=1)

    def is_hint_available(self):
        """ Whether a hint is available """
        if self.hint is not None:
            return True
        else:
            return False

    def get_data(self):
        """ Get the data of the model as a dict """
        return {
            'id': self.pk,
            'quiz': self.quiz,
            'question_module': self.question_module,
            'description': self.description,
            'hint': self.hint,
            'grader_type': self.grader_type,
            'type': self.type,
            'gradable': self.gradable,
            'granularity': self.granularity,
            'granularity_hint': self.granularity_hint,
            'marks': self.marks,
            'attempts': self.attempts,
            'answer_description': self.answer_description
        }

    def get_default_granularity(self, hint=False):
        """
        When courseware module is completed, uncomment the below code to
        define the default granularity for a course

        course_info = self.course.course_info
        if hint:
            if (course_info.granularity_hint is not None and
                course_info.granularity_hint.strip() != ''):
                return course_info.granularity_hint
        else:
            if (course_info.granularity is not None and
                course_info.granularity.strip() != ''):
                return course_info.granularity
        """
        # NOTE on implementation of default granularity:
        # It is very naive implementation since I couldn't get the serializer
        # to accept Blank value for granularity. So UI send "undefined" to backend
        # and backend takes this as a keyword and assignes default value
        # In future we may need granularity in a different format since the current
        # one seems to be inefficient for larger number of attempts
        # Need to comment out lines from courseware models to add granularity
        # to course info.
        granularity = ""
        marks = self.marks
        factor = int(marks/self.attempts)
        for i in range(self.attempts):
            granularity = granularity + str(marks) + ","
            marks = marks - factor
        granularity = granularity + "0"
        #granularity = ((str(self.marks) + ',') * self.attempts) + "0"
        print granularity
        return granularity

    def save(self, *args, **kwargs):
        """ Process some fields before save """
        if self.hint is not None and self.hint.strip() == '':
            self.hint = None
        if (self.granularity is None or
                self.granularity.strip() == '' or
                self.granularity == 'undefined'):
            self.granularity = self.get_default_granularity()
        if (self.granularity_hint is None or
                self.granularity_hint.strip() == '' or
                self.granularity_hint == 'undefined'):
            self.granularity_hint = self.get_default_granularity(hint=True)
        if self.answer_description is None:
            self.answer_description = ''

        super(Question, self).save(*args, **kwargs)

    objects = InheritanceManager()

    class Meta:
        """
        This is not an abstract class
        """
        abstract = False


class DescriptiveQuestion(Question):
    """
    A question with a descriptive answer.
    Ideally, this will be graded manually and the answer field will
    contain a model answer/guidelines.
    """
    answer = models.TextField()

    # set the type field of the question
    def save(self, *args, **kwargs):
        self.type = self.DESCRIPTIVE_ANSWER_QUESTION
        super(DescriptiveQuestion, self).save(*args, **kwargs)


class SingleChoiceQuestion(Question):
    """
    A question which has only 1 of the possible choices as the correct answer
    """
    # JSON Array containing the options
    # E.g.: "['Django', 'Ruby', 'Scala']"
    options = models.TextField(
        help_text='Enter choices one by one')
    answer = models.IntegerField(
        help_text="Answer will be the (0-based) index of the choice above")

    # set the type field of the question
    def save(self, *args, **kwargs):
        self.type = self.SINGLE_CHOICE_QUESTION
        super(SingleChoiceQuestion, self).save(*args, **kwargs)

    def get_answer(self, showToUser=False):
        """
        Return the answer to this question.
        """
        # print self.answer
        # print self.options
        if showToUser:
            options = json.loads(self.options)
            return options[self.answer]
        else:
            return self.answer

    def get_answer_data(self):
        """
            Return answer data packaged up
        """
        selected = [False] * len(json.loads(self.options))
        selected[self.answer] = True

        data = {
            'options': self.options,
            'selected': json.dumps(selected)
        }
        return data


class MultipleChoiceQuestion(Question):
    """
    A question which may have 1 or more correct answers from
    the possible choices
    """
    # JSON Array containing the options
    # E.g.: "['Django', 'Ruby', 'Scala']"
    options = models.TextField(
        help_text='Enter choices seperated by comma (no comma at end): \
            e.g.: choice_1, choice 2, choice 2')
    # JSON Array of Booleans
    # E.g.: "[true, false, true]"
    answer = models.TextField(
        help_text='Answer will be in the form or "[true, false, true]" etc')

    # set the type field of the question
    def save(self, *args, **kwargs):
        self.type = self.MULTIPLE_CHOICE_QUESTION
        super(MultipleChoiceQuestion, self).save(*args, **kwargs)

    def get_answer(self, showToUser=False):
        """
            Return answer for grading if showToUSer not supplied
        """
        if showToUser:
            i = 0
            selected = []
            options = json.loads(self.options)
            print options
            answer = json.loads(self.answer)
            print answer
            for opt in answer:
                if opt:
                    selected.append(options[i])
                i = i + 1
            print selected
            print json.dumps(selected)
            return json.dumps(selected)
        else:
            return self.answer

    def get_answer_data(self):
        """
        Return answer data packaged up
        """
        data = {
            'options': self.options,
            'selected': self.get_answer()
        }
        return data


class FixedAnswerQuestion(Question):
    """
    A question which has a fixed answer to be input in a text field
    """
    # JSON array of acdeptable answers
    answer = models.CharField(max_length=128)

    def get_answer(self, showToUser=False):
        """
        Return the answer to this question.
        Ideally we want that we should set the answer_shown in question_history
            whenever this is called, but that is expensive. So, wherever we
            call get_answer, set answer_shown = True and save.
        """
        print self.answer
        return json.loads(self.answer)
        # TODO : replace the function below to work with a json string
        #if showToUser:
        #    answer = self.answer
        #    if len(self.answer.split(',')) > 1:
        #        answer = string.replace(answer, ',', ', ')
        #    return answer
        #else:
        #    return self.answer.split(',')

    def get_answer_data(self):
        """
        Return answer data packaged up
        """
        data = {
            'answer': self.get_answer()
        }
        return data

    # set the type field of the question
    def save(self, *args, **kwargs):
        self.type = self.FIXED_ANSWER_QUESTION
        super(FixedAnswerQuestion, self).save(*args, **kwargs)


class ProgrammingQuestion(Question):
    """
    A question which requires the submission of a file to be graded
    according to the command given with it
    """
    num_testcases = models.IntegerField()
    command = models.TextField()  # command to compile and run the submission
    # string of file extensions separated by comma
    acceptable_languages = models.TextField()

    # set the type field of the question
    def save(self, *args, **kwargs):
        self.type = self.PROGRAMMING_QUESTION
        super(ProgrammingQuestion, self).save(*args, **kwargs)


class Testcase(models.Model):
    """
    A testcase is one of the many inputs against which a ProgrammingQuestion is
    to be evaluated
    """
    question = models.ForeignKey(
        ProgrammingQuestion,
        related_name='Testcase_ProgrammingQuestion')
    input_text = models.TextField()
    correct_output = models.TextField()


class QuestionHistory(models.Model):
    """
    This class captures the history of a question associated with each student
    """
    question = models.ForeignKey(
        Question,
        related_name='QuestionHistory_Question')
    student = models.ForeignKey(User, related_name='QuestionHistory_User')
    attempts = models.IntegerField(default=0)
    marks = models.FloatField(default=0.0)
    NOT_ATTEMPTED = 'N'
    ATTEMPTED_ONCE = 'O'
    AWAITING_RESULTS = 'A'
    SOLVED = 'S'
    status_codes = (
        (NOT_ATTEMPTED, 'Not Attempted'),
        (ATTEMPTED_ONCE, 'Attempted atleast once'),
        (AWAITING_RESULTS, 'Awaiting Results'),
        (SOLVED, 'Solved')
    )
    status = models.CharField(max_length=1, choices=status_codes, default='N')
    hint_taken = models.BooleanField(default=False)
    answer_shown = models.BooleanField(default=False)

    class Meta:
        """
        question and student combined should be unique
        """
        unique_together = ("question", "student")


class Queue(TimeKeeper):
    """
    This is a utility class to store objects that we need to perform actions
    on asynchronously - email, notification, grading of programming question
    """
    object_id = models.TextField()  # id of notification or email or submission
    is_processed = models.BooleanField(default=False)
    EMAIL = 'E'
    NOTIFICATION = 'N'
    SUBMISSION = 'S'
    object_types = (
        (EMAIL, 'Email'),
        (NOTIFICATION, 'Notification'),
        (SUBMISSION, 'Submission')
    )
    object_type = models.CharField(
        max_length=1,
        choices=object_types,
        default='E')
    info = models.TextField()  # extra information


class Submission(TimeKeeper):
    """
    A submission is added when a student answers the question. Depending on the
    type of grader being used, the evaluation may be instant or waiting
    """
    #course = models.ForeignKey(
    #    Course,
    #    related_name="Submission_Course",
    #    db_index=True
    #)
    question = models.ForeignKey(Question, related_name='Submission_Question')
    student = models.ForeignKey(User, related_name='Submission_User')
    grader_type = models.CharField(
        max_length=1,
        choices=Question.GRADER_TYPES,
        default='D')  # so its easy to know rather than going to question
    answer = models.TextField()
    # No queue for the time being
    #queue_id = models.ForeignKey(Queue, related_name='Submission_Queue')
    AWAITING_RESULTS = 'A'
    DONE = 'D'
    status_codes = (
        (AWAITING_RESULTS, 'Awaiting Results'),
        (DONE, 'Done')
    )
    status = models.CharField(
        max_length=1,
        choices=status_codes,
        default=AWAITING_RESULTS)
    feedback = models.TextField(default='')  # feedback from the grader
    result = models.FloatField(default=0.0)  # marks given to this submission
    is_correct = models.BooleanField(default=False)
    is_plagiarised = models.BooleanField(default=False)  # plagiarism checking
    # has been checked for plagiarism or not
    has_been_checked = models.BooleanField(default=False)


@receiver_subclasses(pre_save, Question, "question_pre_save")
def update_question_stats_pre_save(sender, **kwargs):
    """ Increase question count by 1 and max_marks"""
    instance = kwargs['instance']
    if instance.pk is not None:  # update
        instance.quiz.update_score(-1*(instance.marks))


@receiver_subclasses(post_save, Question, "question_post_save")
def update_question_stats_post_save(sender, **kwargs):
    """ Increase question count by 1 and max_marks"""
    instance = kwargs['instance']
    if kwargs['created']:  # create
        instance.quiz.questions += 1
        instance.question_module.questions += 1
    instance.quiz.save()
    instance.quiz.update_score(instance.marks)
    instance.question_module.save()


@receiver_subclasses(pre_delete, Question, "question_pre_delete")
def update_question_stats_on_delete(sender, **kwargs):
    """ Decrease question count by 1 and max_marks"""
    instance = kwargs['instance']
    if type(instance) != Question:
        # This is necessary otherwise it is called twice: once for parent class
        #   and other for subclass
        instance.quiz.questions -= 1
        instance.quiz.save()
        instance.quiz.update_score(-1*(instance.marks))
        instance.question_module.questions -= 1
        instance.question_module.save()


@receiver(post_save, sender=QuestionModule)
def update_question_module_stats_post_save(sender, **kwargs):
    """ Increase question module count by 1"""
    instance = kwargs['instance']
    if kwargs['created']:  # create
        instance.quiz.question_modules += 1
        instance.quiz.save()


@receiver(pre_delete, sender=QuestionModule)
def update_question_module_stats_on_delete(sender, **kwargs):
    """ Decrease question module count by 1"""
    instance = kwargs['instance']
    instance.quiz.question_modules -= 1
    instance.quiz.save()


#TODO add the above classes for question modules

@receiver(pre_delete, sender=QuestionHistory)
def update_concept_history_on_delete(sender, **kwargs):
    """Update quizhistory marks"""
    instance = kwargs['instance']
    quiz_history, created = QuizHistory.objects.get_or_create(
        quiz=instance.question.quiz, user=instance.student)
    quiz_history.update_score(-1*(instance.marks))
