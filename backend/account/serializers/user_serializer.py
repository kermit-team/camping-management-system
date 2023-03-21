import django.contrib.auth.password_validation as validators
from django.contrib.auth.models import Group
from django.core import exceptions

from rest_framework import serializers

from account.models import User
from .group_serializer import GroupSerializer


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

    def validate(self, data):
        groups = data.pop('groups', None)
        password = data.get('password')
        user = User(**data)
        if groups is not None:
            data['groups'] = groups        

        errors = dict() 
        try:
            validators.validate_password(password=password, user=user)
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)
         
        if errors:
            raise serializers.ValidationError(errors)
          
        return super(UserRegistrationSerializer, self).validate(data)

class UserRequestSerializer(serializers.ModelSerializer):

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

class UserResponseSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = (
            'id',
            'url',
            'email',
            'first_name',
            'last_name',
            'is_active',
            'is_staff',
            'is_superuser',
            'phone_number',
            'avatar',
            'groups',
        )
