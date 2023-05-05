from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from . import serializers
from rest_framework.response import Response


# Create your views here.
@extend_schema(tags=['Authentication'])
@extend_schema_view()
class AuthenticationView(viewsets.ViewSet): 

    @extend_schema(
        auth=[],
        request=serializers.LoginSerializer,
        parameters=None,
        responses=None
    ) 
    @action(
        detail=False, 
        methods=['post'], 
        url_path='login', 
        permission_classes=[AllowAny]
    )
    def login(self, request, *args, **kwargs):
        """
        Login for users

        POST auth/login
        """
        data = request.data
        serializer = serializers.LoginSerializer(context={'request': request}, data=data)
        if serializer.is_valid():
            instance = serializer.save()
            return Response(instance, status=status.HTTP_200_OK)
        else:
            return Response(serializer.get_error_response(), status=400)