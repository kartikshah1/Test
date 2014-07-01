from rest_framework import serializers

from quiz_template import models


class QuizSerializer(serializers.ModelSerializer):

    """
    Serialization of Quiz model
    """
    class Meta:

        """ Meta """
        model = models.Quiz
        fields = ('id', 'title', 'questions', 'marks')
        read_only_fields = ('marks', 'questions')


class QuestionMasterSerializer(serializers.ModelSerializer):

    """
    Serialization of Question_Master model
    """
    class Meta:

        """ Meta """
        model = models.Question_Master


class QuestionScqSerializer(serializers.ModelSerializer):

    """
    Serialization of Question_Scq model
    """
    class Meta:

        """ Meta """
        model = models.Question_Scq

class QuestionMcqSerializer(serializers.ModelSerializer):

    """
    Serialization of Question_Mcq model
    """
    class Meta:

        """ Meta """
        model = models.Question_Mcq


class QuestionFixSerializer(serializers.ModelSerializer):

    """
    Serialization of Question_Fix model
    """
    class Meta:

        """ Meta """
        model = models.Question_Fix


class QuestionDesSerializer(serializers.ModelSerializer):

    """
    Serialization of Question_Des model
    """
    class Meta:

        """ Meta """
        model = models.Question_Des


class QuestionModuleSerializer(serializers.ModelSerializer):

    """
    Serialization of Question_Module model
    """
    class Meta:

        """ Meta """
        model = models.Question_Module
        fields = ('id', 'static_text', 'title', 'quiz')


class UserSubmissionsSerializer(serializers.ModelSerializer):

    """
    Serialization of UserSubmssions model
    """
    class Meta:

        """ Meta """
        model = models.User_Submissions
        read_only_fields = ('attempts', 'marks', 'status')

class FrontEndQuestionSerializer(serializers.Serializer):
    """
    Serializer to show all Question_Master data and user submission together
    """
    id = serializers.IntegerField()
    marks = serializers.CharField()
    attempts = serializers.IntegerField()
    text = serializers.CharField()
    is_hint_available = serializers.BooleanField(default=False)
    type = serializers.CharField(max_length=3)
    user_attempts = serializers.IntegerField(default=0)
    user_marks = serializers.FloatField(default=0.0)
    user_status = serializers.CharField(max_length=1)
    hint_taken = serializers.BooleanField(default=False)
    hint = serializers.CharField(default=None)
    answer_shown = serializers.BooleanField(default=False)
    answer = serializers.CharField(default=None)
    options = serializers.CharField(default=None)
    explaination = serializers.CharField(default=None)


class FrontEndSubmissionSerializer(serializers.Serializer):
    """
    Serialization utility to send back a submission to the front end
    """
    status = serializers.CharField()
    marks = serializers.FloatField()
    attempts_remaining = serializers.IntegerField()
    answer = serializers.CharField(default=None)
    explaination = serializers.CharField(default=None)

class AnswerSubmitSerializer(serializers.Serializer):
    """
    Serialization utility for submission of an answer
    """
    answer = serializers.CharField()