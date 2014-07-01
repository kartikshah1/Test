"""Serializers for Concept Models"""

from rest_framework import serializers
from concept import models


class ConceptQuizHistorySerializer(serializers.ModelSerializer):
    """Serializer for ConceptQuizHistory"""
    class Meta:
        model = models.ConceptQuizHistory


class ConceptDocumentHistorySerializer(serializers.ModelSerializer):
    """Serializer for ConceptDocumentHistory"""
    class Meta:
        model = models.ConceptDocumentHistory
