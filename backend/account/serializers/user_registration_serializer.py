import django.contrib.auth.password_validation as validators
from django.core import exceptions

from rest_framework import serializers

from account.models import User
from .group_response_serializer import GroupResponseSerializer


class UserRegistrationSerializer(serializers.ModelSerializer):
    groups = GroupResponseSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'first_name',
            'last_name',
            'id_card',
            'groups',
        )

    def validate(self, data):
        groups = data.pop('groups', None)
        password = data.get('password')
        user = User(**data)
        if groups:
            user.groups.set(groups)
            data['groups'] = groups        

        errors = dict() 
        try:
            validators.validate_password(password=password, user=user)
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)
         
        if errors:
            raise serializers.ValidationError(errors)
          
        return super(UserRegistrationSerializer, self).validate(data)
