from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.timezone import now
from django.db.models import CharField, Value as V, Q, Sum
from helpers.serializers import (
    ModelSerializer,
    Serializer
)
from helpers.global_utils import (
    get_tokens_for_user
)


class UserDetailsSerializer(ModelSerializer):
     class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'email'
        )


class LoginSerializer(ModelSerializer):
    """
    LoginSerializer
    """

    username = serializers.CharField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=3)

    class Meta:
        model = User
        fields = ('username', 'password')

    def validate(self, attrs):
        errors = dict()  
        request = self.context.get('request')
        user = authenticate(request, username=attrs['username'], password=attrs['password'])
        if user is None:
            errors['generic'] = 'Username or password is invalid.'

        # Check if it has errors
        if errors:
            raise serializers.ValidationError(errors)
        return user

    def save(self, **kwargs): 
        request = self.context.get('request')
        user = self.validated_data 
        user.last_login = now() 
        user.save()

        return {
            **UserDetailsSerializer(user).data,
            'token': get_tokens_for_user(user)
        }