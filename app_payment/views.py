from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# Create your views here.
from drf_spectacular.utils import extend_schema, extend_schema_view
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.types import OpenApiTypes

    
from rest_framework.renderers import JSONRenderer
from datetime import datetime
import json, base64, logging
import requests
from threading import Thread
from django.db import transaction
from . import serializers
from .models import (
    Payment,
    Currency
)
from helpers.global_utils import (
    PAGINATED_PARAMETERS,
    search_result
)
from helpers.paginator import Paginator


@extend_schema(tags=['Payments'])
@extend_schema_view()
class PaymentViews(viewsets.ViewSet):

    @extend_schema(
        request=serializers.CreatePaymentSerializer,
        parameters=None,
        responses=None
    ) 
    @action(
        detail=False,
        permission_classes=[IsAuthenticated],
        methods=["post"],
        url_path="create",
    )
    def create_payment(self, request):
        """
        Create My Payment

        POST payment/create
        """
        data = request.data
        serializer = serializers.CreatePaymentSerializer(context={'request': request}, data=data)
        if serializer.is_valid():
            payment = serializer.save()
            return Response({
                'statusCode': status.HTTP_201_CREATED,
                'message': ['Payment successfully created'],
                'data': serializers.PaymentSerializer(payment).data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.get_error_response(), status=400)

    @extend_schema(
        request=None,
        parameters=[
            *PAGINATED_PARAMETERS,
            OpenApiParameter(
                name="search",
                location=OpenApiParameter.QUERY,
                description="Search Reference Code",
                type=str,
                required=False,
                default=''
            ),
            OpenApiParameter(
                name="currencyCode",
                location=OpenApiParameter.QUERY,
                description="Currency Code",
                type=str,
                required=False,
                default=''
            )
        ],
        responses=None
    ) 
    @action(
        detail=False,
        permission_classes=[IsAuthenticated],
        methods=["get"],
        url_path="list",
    )
    def get_payment_list(self, request):
        """
        Get My Payment List

        GET payment/list
        """
        data = request.GET
        _search = data.get('search')
        _currency_code = data.get('currencyCode')
        currency = None

        if _currency_code:
            try:
                currency = Currency.objects.get(code=_currency_code)
            except Exception as e:
                return Response({
                    'statusCode': 404,
                    'message': [
                        'Currency is not existing.'
                    ]
                }, status=status.HTTP_404_NOT_FOUND)
            
        queryset = Payment.objects.filter(user=request.user)
        if currency: 
            queryset = queryset.filter(currency=currency)

        if _search:
            orm_lookups = [
                'reference_code__icontains'
            ]
            queryset = search_result(queryset, _search, orm_lookups, limit_data=False)

        paginated_queryset = Paginator(
            queryset, 
            request
        ).paginate(
            serializer=serializers.PaymentSerializer
        ) 
        return Response({
            'statusCode': 200,
            'data': paginated_queryset
        }, status=200)

    @extend_schema(
        request=None,
        parameters=None,
        responses=None
    ) 
    @action(
        detail=True,
        permission_classes=[IsAuthenticated],
        methods=["patch"],
        url_path="paid",
    )
    def update_payment(self, request, pk):
        """
        Payment Paid

        PATCH payment/{id}/paid
        """
        try:
            payment = Payment.objects.get(pk=pk)
        except Exception as e:
            return Response({
                'statusCode': 404,
                'message': [
                    'Payment not found.'
                ]
            }, status=status.HTTP_404_NOT_FOUND) 
        
        if payment.is_paid:
            return Response({
                'statusCode': 400,
                'message': [
                    'This payment is already paid.'
                ]
            }, status=status.HTTP_400_BAD_REQUEST) 
        
        payment.is_paid = True
        payment.paid_date = datetime.today().date()
        payment.save()
        return Response({
            'statusCode': 200,
            'message': [
                'Your payment is successfully paid.'
            ]
        }, status=status.HTTP_200_OK) 