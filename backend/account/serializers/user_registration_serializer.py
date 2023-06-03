from django.contrib.auth import password_validation as validators
from django.core import exceptions
from rest_framework import serializers

from account.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'first_name',
            'last_name',
            'groups',
        )

    def validate(self, attrs):
        groups = attrs.pop('groups', None)
        password = attrs.get('password')
        user = User(**attrs)
        if groups:
            attrs['groups'] = groups

        errors = {}
        try:
            validators.validate_password(password=password, user=user)
        except exceptions.ValidationError as e:
            errors['password'] = [e.messages]

        if errors:
            raise serializers.ValidationError(errors)

        return super(UserRegistrationSerializer, self).validate(attrs)
