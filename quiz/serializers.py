"""
Serializer classes for Django Rest Framework
"""

from rest_framework import serializers

from quiz import models


class QuizSerializer(serializers.ModelSerializer):
    """
    Serialization of Quiz model
    """
    class Meta:
        """ Meta """
        model = models.Quiz
        read_only_fields = ('marks', 'questions', 'question_modules')


class QuestionModuleSerializer(serializers.ModelSerializer):
    """
    Serialization of QuestionModule model
    """
    class Meta:
        """ Meta """
        model = models.QuestionModule


class QuestionSerializer(serializers.ModelSerializer):
    """
    Serialization of Question model
    """
    is_hint_available = serializers.Field(source='is_hint_available')

    class Meta:
        """ Meta """
        model = models.Question
        exclude = ('gradable', 'hint', 'answer_description', 'granularity',
                   'granularity_hint')


class FixedAnswerQuestionSerializer(serializers.ModelSerializer):
    """
    Serialization of FixedAnswerQuestion model
    """
    class Meta:
        """ Meta """
        model = models.FixedAnswerQuestion
        exclude = ('question_module', 'quiz')


class SingleChoiceQuestionSerializer(serializers.ModelSerializer):
    """
    Serialization of SingleChoiceQuestion model
    """
    class Meta:
        """ Meta """
        model = models.SingleChoiceQuestion
        exclude = ('question_module', 'quiz')


class MultipleChoiceQuestionSerializer(serializers.ModelSerializer):
    """
    Serialization of SingleChoiceQuestion model
    """
    class Meta:
        """ Meta """
        model = models.MultipleChoiceQuestion
        exclude = ('question_module', 'quiz')


class SubmissionSerializer(serializers.ModelSerializer):
    """
    Serialization of FixedAnswerQuestion model
    """
    class Meta:
        """ Meta """
        model = models.Submission
        read_only_fields = ('status', 'is_plagiarised', 'has_been_checked')


class FrontEndQuestionSerializer(serializers.Serializer):
    """
    Serializer to show all Question data and user history together
    """
    id = serializers.IntegerField()
    marks = serializers.FloatField(default=0.0)
    attempts = serializers.IntegerField()
    description = serializers.CharField()
    is_hint_available = serializers.BooleanField(default=False)
    type = serializers.CharField(max_length=1)
    user_attempts = serializers.IntegerField(default=0)
    user_marks = serializers.FloatField(default=0.0)
    user_status = serializers.CharField(max_length=1)
    hint_taken = serializers.BooleanField(default=False)
    hint = serializers.CharField(default=None)
    answer_shown = serializers.BooleanField(default=False)
    answer = serializers.CharField(default=None)
    answer_description = serializers.CharField(default=None)
    options = serializers.CharField(default=None)


class FrontEndSubmissionSerializer(serializers.Serializer):
    """
    Serialization utility to send back a submission to the front end
    """
    status = serializers.CharField()
    result = serializers.FloatField()
    is_correct = serializers.BooleanField()
    attempts_remaining = serializers.IntegerField()
    answer = serializers.CharField(default=None)
    answer_description = serializers.CharField(default=None)


class PlagiarismSerializer(serializers.Serializer):
    """
    Serialization utility for setting a submission to be plagiarised
    """
    is_plagiarised = serializers.BooleanField()


class AnswerSubmitSerializer(serializers.Serializer):
    """
    Serialization utility for submission of an answer
    """
    answer = serializers.CharField()


class AdminQuestionSerializer(serializers.ModelSerializer):
    """ All fields of Question model """
    class Meta:
        """ Meta """
        model = models.Question
