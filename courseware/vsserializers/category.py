from rest_framework import serializers
from courseware.models import ParentCategory, Category
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """ Serializer for django.contrib.auth.User """
    class Meta:
        """Meta"""
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class ParentCategorySerializer(serializers.ModelSerializer):
    """Serializer for ParentCategory Model"""
    class Meta:
        """Meta"""
        model = ParentCategory


class CategorySerializer(serializers.ModelSerializer):
    """serializer for the category class"""
    # TODO: content_developers = UserSerializer(many=True)

    class Meta:
        """Meta"""
        model = Category
        exclude = ('content_developers',)
