"""
    Serializers for Course, CourseHistory and CourseInfo Models
"""

from rest_framework import serializers
from courseware.models import Course, Offering, CourseHistory, CourseInfo


class CourseInfoSerializer(serializers.ModelSerializer):
    """serializer for the courseinfo class"""
    class Meta:
        """Meta"""
        model = CourseInfo
        read_only_fields = ('is_published',)


class CourseSerializer(serializers.ModelSerializer):
    """serializer for the course class"""
    course_info = CourseInfoSerializer(required=False)

    class Meta:
        """Meta"""
        model = Course
        exclude = ('pages', 'max_score')
        read_only_fields = ('forum', 'type', 'playlist', 'page_playlist')


class OfferingSerializer(serializers.ModelSerializer):
    """Serializer for the offering model"""
    course_info = CourseInfoSerializer(required=False)

    class Meta:
        model = Offering
        exclude = ('pages', 'shortlisted_courses', 'max_score')
        read_only_fields = ('forum', 'type', 'playlist', 'page_playlist')


class CourseHistorySerializer(serializers.ModelSerializer):
    """Serializer for CourseHistory Model"""
    class Meta:
        """Meta"""
        model = CourseHistory
        fields = ('course', 'user', 'grade', 'score')
