"""
    Serializers for the video API
"""

from rest_framework import serializers
from video import models


class MarkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Marker


class SectionMarkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SectionMarker


class QuizMarkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuizMarker


class MarkerListingField(serializers.RelatedField):
    def to_native(self, value):
        value = models.Marker.objects.filter(pk=value.id).select_subclasses()[0]
        if isinstance(value, models.SectionMarker):
            return SectionMarkerSerializer(value).data
        elif isinstance(value, models.QuizMarker):
            return QuizMarkerSerializer(value).data
        #elif isinstance(value, models.Marker):
        #    return 'Marker came instead'
        else:
            print "Unknown Marker found in video. %s" % (value)
            return {}


class VideoSerializer(serializers.ModelSerializer):
    markers = MarkerListingField(many=True)
    video_file = serializers.Field(source='get_video_file')
    other_file = serializers.Field(source='get_other_file')

    class Meta:
        model = models.Video
        fields = ('id', 'title', 'content', 'upvotes', 'downvotes', 'video_file', 'markers', 'other_file', 'duration')


class AddVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Video
        exclude = ('video_file', 'other_file')


class VideoHistorySerializer(serializers.ModelSerializer):
    """Serializer for VideoHistory"""
    class Meta:
        model = models.VideoHistory
