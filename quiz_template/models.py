from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from model_utils.managers import InheritanceManager
from django.db.models.signals import pre_save, post_save, pre_delete
import json
from util.methods import receiver_subclasses


class Quiz(models.Model):

    """Quiz
        title: String
            --title of Quiz
        questions: int
            -- number of questions in Quiz
        marks: int
            -- total max marks
    """
    title = models.TextField()
    questions = models.IntegerField(default=0)
    marks = models.FloatField(default=0)


class Question_Module(models.Model):

    """Question Module for common question Title

        static_text: String | Null
            --shared text of multiple questions
        title: String
            --shared title of multiple questions
        quiz: Quiz
            -- each question/question set belongs to a quiz
    """
    static_text = models.TextField(default="")
    title = models.TextField()
    quiz = models.ForeignKey(Quiz, related_name="question_modules")


class Question_Master(models.Model):

    """Master Question Table

    Stores:
    -------
    type: String [ mcq | des | fix ]
        --Type of Question
    title: String | Null
        --Title of the question
    text: String
        --Question Text
    module: Question_Module
        -- For storing title, common text in set of questions
    marks: Stringified JSON Array of Numbers
        -- For storing different granularity and marks
    hint: String | Null
        -- Hint for the question
    answer: String
        -- IF SCQ - String(int) which denotes correct
        -- IF MCQ - Array of integers to denote choices
        -- IF FIX - Different sets of possible answers
        -- IF DES - Answer of the question
    """
    SINGLE_CHOICE_QUESTION = 'scq'
    MULTIPLE_CHOICE_QUESTION = 'mcq'
    FIXED_ANSWER_QUESTION = 'fix'
    DESCRIPTIVE_ANSWER_QUESTION = 'des'
    QUESTION_TYPES = (
        (SINGLE_CHOICE_QUESTION, 'Single Choice Question'),
        (MULTIPLE_CHOICE_QUESTION, 'Multiple Choice Question'),
        (FIXED_ANSWER_QUESTION, 'Fixed Answer Question'),
        (DESCRIPTIVE_ANSWER_QUESTION, 'Descriptive Answer Question'),
    )

    type = models.CharField(max_length=3, choices=QUESTION_TYPES)
    text = models.TextField()
    module = models.ForeignKey(
        Question_Module, related_name='module_questions')
    marks = models.TextField()
    hint = models.TextField(default="")
    answer = models.TextField()
    attempts = models.IntegerField(default=0)
    objects = InheritanceManager()

    def cleanup(self):
        if self.type not in ["scq", "mcq", "des", "fix"]:
            raise ValidationError("Question type " +
                                  self.type +
                                  " is not supported")

    def save(self, *args, **kwargs):
        """Processing some fields before save"""
        marks = json.loads(self.marks)
        self.attempts = len(marks)
        super(Question_Master, self).save(*args, **kwargs)

    def is_hint_available(self):
        if self.hint is None:
            return False
        if self.hint is not None and self.hint.strip() == '':
            return False
        else:
            return True

    def get_max_marks(self):
        marks = json.loads(self.marks)
        return marks[0]


class Question_Scq(Question_Master):

    """Question_Scq for question with choices - SCQ
        options: Stringified JSON Array
            --choices for question
        explainations: Stringified JSON Array
            --explainations for wrong answers
        default: String
            --default explainations to be used
    """
    options = models.TextField()
    explainations = models.TextField(default="[]")
    default_explanation_correct = models.TextField(default="Answer Correct")
    default_explanation_wrong = models.TextField(default="Answer Wrong")

    def save(self, *args, **kwargs):
        self.type = self.SINGLE_CHOICE_QUESTION
        super(Question_Scq, self).save(*args, **kwargs)

    def get_answer(self):
        options = json.loads(self.options)
        return options[int(self.answer)]


class Question_Mcq(Question_Master):

    """Question_Choice for question with choices - SCQ
        options: Stringified JSON Array
            --choices for question
        explainations: Stringified JSON Array
            --explainations for wrong answers
        default: String
            --default explainations to be used
    """
    options = models.TextField()
    explainations = models.TextField(default="[]")
    default_explanation_correct = models.TextField(default="Answer Correct")
    default_explanation_wrong = models.TextField(default="Answer Wrong")

    def save(self, *args, **kwargs):
        self.type = self.MULTIPLE_CHOICE_QUESTION
        super(Question_Mcq, self).save(*args, **kwargs)

    def get_answer(self):
        options = json.loads(self.options)
        answers = json.loads(self.answer)
        answer = ""
        for ans, opt in zip(answers, options):
            if ans:
                answer += opt + "\n"
        print answer
        return answer


class Question_Fix(Question_Master):

    """Question_Fix

        explainations: Stringified JSON Array
            --explainations for wrong answers
        default: String
            --default explainations to be used
     """
    explainations = models.TextField(default="[]")
    default_explanation_correct = models.TextField(default="Answer Correct")
    default_explanation_wrong = models.TextField(default="Answer Wrong")

    def save(self, *args, **kwargs):
        self.type = self.FIXED_ANSWER_QUESTION
        super(Question_Fix, self).save(*args, **kwargs)

    def get_answer(self):
        return self.answer


class Question_Des(Question_Master):

    """Question_Des

        default: String
            --default explainations to be used
     """
    default_explanation_correct = models.TextField(default="Answer Correct")
    default_explanation_wrong = models.TextField(default="Answer Wrong")

    def save(self, *args, **kwargs):
        self.type = self.DESCRIPTIVE_ANSWER_QUESTION
        super(Question_Des, self).save(*args, **kwargs)

    def get_answer(self):
        return self.answer


class User_Submissions(models.Model):

    """UserSubmissions for answer submission by student

        question: Question_Master
            -- question for which submission is made
        user: User
            -- who made the submission
        answer: String
            -- answer in format as required by different type of questions
        attempts: Integer
            -- number of attempts
        marks: Float
            -- marks scored in the question by user
        status: Char
            -- IF N - Not attempted even once
            -- IF A - Attempted and attempts remain, but wrong
            -- IF C - Correct answer, no changes now
            -- IF W - all attempts over, answer shown
    """
    question = models.ForeignKey(Question_Master)
    user = models.ForeignKey(User)
    answer = models.TextField(default="")
    attempts = models.IntegerField(default=0)
    marks = models.FloatField(default=0.0)
    hint_taken = models.BooleanField(default=False)
    explaination = models.TextField(default="")
    NOT_ATTEMPTED = 'N'
    ATTEMPTED = 'A'
    CORRECT = 'C'
    WRONG = 'W'
    status_codes = (
        (NOT_ATTEMPTED, 'Not Attempted'),
        (ATTEMPTED, 'Attempted'),
        (CORRECT, 'Correct'),
        (WRONG, 'Wrong')
    )
    status = models.CharField(max_length=1, choices=status_codes, default='N')

    def is_answer_shown(self):
        if self.status == self.CORRECT or self.status == self.WRONG:
            return True
        else:
            return False

    class Meta:

        """
        question and user combined should be unique
        """
        unique_together = ("question", "user")


@receiver_subclasses(pre_save, Question_Master, "question_pre_save")
def update_question_stats_pre_save(sender, **kwargs):
    """ Decrease by previous marks"""
    instance = kwargs['instance']
    if(type(instance) == Question_Master):
        if instance.pk is not None:
            instance.module.quiz.marks -= json.loads(instance.marks)[0]
            instance.module.quiz.save()


@receiver_subclasses(post_save, Question_Master, "question_post_save")
def update_question_stats_post_save(sender, **kwargs):
    """ Increase question count by 1 and max_marks"""
    instance = kwargs['instance']
    if(type(instance) == Question_Master):
        if kwargs['created']:
            instance.module.quiz.questions += 1
        instance.module.quiz.marks += json.loads(instance.marks)[0]
        instance.module.quiz.save()


@receiver_subclasses(pre_delete, Question_Master, "question_pre_delete")
def update_question_stats_on_delete(sender, **kwargs):
    """ Decrease question count by 1 and max_marks"""
    instance = kwargs['instance']
    if (type(instance) == Question):
        instance.module.quiz.questions -= 1
        instance.module.quiz.marks -= json.loads(instance.marks)[0]
        instance.module.quiz.save()
