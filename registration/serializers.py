"""
Serializers for the registration API
"""

from rest_framework import serializers
from registration import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('username', 'first_name', 'last_name', 'email')

    ##TODO More Validation
    def validate(self, attrs):
        print "VALIDATION CALLED"
        try:
            email = attrs['email']
        except KeyError:
            raise serializers.ValidationError("Email field is required")
        return attrs

    ##TODO: This is a hack to throw in validation errors
    ## else the user is returned a empty string
    def get_validation_exclusions(self):
        pass


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('password')
