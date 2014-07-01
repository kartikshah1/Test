"""
    Serializers for document app.
"""

from rest_framework import serializers
from document.models import Document, Section
from courseware.models import SHORT_TEXT


class DocumentSerializer(serializers.ModelSerializer):
    """ModelSerializer for Document class"""
    class Meta:
        model = Document
        exclude = ('uid',)


class SectionSerializer(serializers.ModelSerializer):
    """ModelSerializer for Section"""
    class Meta:
        """Meta"""
        model = Section


class AddSectionSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=SHORT_TEXT)
    description = serializers.CharField()
