"""
Serializers for the courseware API
"""

from rest_framework import serializers

from courseware import models

from video.serializers import VideoSerializer
from quiz.serializers import QuizSerializer
from document.serializers import DocumentSerializer


class AddGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Group
        exclude = ('pages', 'course')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Group
        exclude = ('pages',)


class ConceptSerializer(serializers.ModelSerializer):
    """
    Serializer for Concept
    """
    videos = VideoSerializer(many=True)
    quizzes = QuizSerializer(many=True)
    pages = DocumentSerializer(many=True)

    class Meta:
        """
        Defining model
        """
        model = models.Concept
        fields = ('id', 'title', 'description', 'image', 'playlist', 'is_published')
        #fields = ('id', 'group', 'title', 'image', 'playlist')


class ConceptDataPlaylistSerializer(serializers.Serializer):
    """
    Serializer to create the playlist to send to the concept page
    """
    id = serializers.IntegerField()
    title = serializers.CharField(default='title not specified')
    seen_status = serializers.BooleanField(default=False)
    toc = serializers.CharField()
    url = serializers.CharField()


class GroupPlaylistSerializer(serializers.Serializer):
    """
    Serializer for the playlist of a group_playlist
    """
    id = serializers.IntegerField()
    title = serializers.CharField()


class ConceptDataSerializer(serializers.Serializer):
    """
    Selrializer to send the data required for the
    concept page
    """
    id = serializers.IntegerField()
    title = serializers.CharField(default='title_not_specified')
    description = serializers.CharField(default='description_not_provided')
    group = serializers.IntegerField(default=0)
    group_title = serializers.CharField(default='group_not_spefified')
    course = serializers.IntegerField(default=0)
    course_title = serializers.CharField(default='course_not_specified')
    playlist = ConceptDataPlaylistSerializer(many=True)
    current_video = serializers.IntegerField(default=-1)
    group_playlist = GroupPlaylistSerializer(many=True)
    course_playlist = GroupPlaylistSerializer(many=True)
    title_document = DocumentSerializer()


class ConceptHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for ConceptHistory
    """
    class Meta:
        """
        Defining model
        """
        model = models.ConceptHistory


class AddQuizSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=models.SHORT_TEXT)
