import django.contrib.auth.password_validation as validators
from django.core import exceptions

from rest_framework import serializers

from account.models import User
from .group_response_serializer import GroupResponseSerializer


class UserRequestSerializer(serializers.ModelSerializer):
    groups = GroupResponseSerializer(many=True, read_only=True)
    
    class Meta:
        model = User
        fields = (
            'password',
            'first_name',
            'last_name',
            'phone_number',
            'avatar',
            'groups',
        )

    def validate(self, data):
        groups = data.pop('groups', None)
        password = data.get('password')
        user = User(**data)
        if groups is not None:
            data['groups'] = groups   
        
        errors = dict() 
        if password is not None:
            try:
                validators.validate_password(password=password, user=user)
            
            except exceptions.ValidationError as e:
                errors['password'] = list(e.messages)
         
        if errors:
            raise serializers.ValidationError(errors)
          
        return super(UserRequestSerializer, self).validate(data)