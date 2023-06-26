from django.contrib.auth import password_validation as validators
from django.core import exceptions
from rest_framework import serializers

from account.models import User


class UserRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'password',
            'first_name',
            'last_name',
            'id_card',
            'phone_number',
            'avatar',
            'groups',
        )

    def validate(self, attrs):
        groups = attrs.pop('groups', None)
        password = attrs.get('password')
        user = User(**attrs)
        if groups:
            attrs['groups'] = groups

        errors = {}
        if password:
            try:
                validators.validate_password(password=password, user=user)

            except exceptions.ValidationError as e:
                errors['password'] = [e.messages]

        if errors:
            raise serializers.ValidationError(errors)

        return super(UserRequestSerializer, self).validate(attrs)
