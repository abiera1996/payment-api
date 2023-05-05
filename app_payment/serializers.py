from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.utils.timezone import now
from django.db.models import CharField, Value as V, Q, Sum
from django.db import transaction
from helpers.serializers import (
    ModelSerializer,
    Serializer
)
from .models import (
    Payment,
    Currency
)
from datetime import datetime
from helpers.global_utils import (
    id_generator
)
import string

class UserDetailsSerializer(ModelSerializer):
     class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email'
        )


class CurrencySerializer(ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class PaymentSerializer(ModelSerializer):
    user = UserDetailsSerializer()
    currency = CurrencySerializer()

    class Meta:
        model = Payment
        fields = '__all__'


class CreatePaymentSerializer(ModelSerializer):

    class Meta:
        model = Payment
        fields = ('currency', 'amount')

    def validate(self, attrs):
        errors = dict()  
        request = self.context.get('request')
        user = request.user
        payment = Payment(user=request.user, currency=attrs['currency'], amount=attrs['amount'])
        is_valid, message = payment.check_user_payment_availability()  # will raise ValidationError if amount limit is exceeded
        if not is_valid:
            errors['generic'] = message
        attrs['payment'] = payment
        # Check if it has errors
        if errors:
            raise serializers.ValidationError(errors)
        return attrs

    def save(self, **kwargs): 
        request = self.context.get('request')
        data = dict(list(self.validated_data.items()))
        with transaction.atomic():
            payment = data['payment']
            code = id_generator(size=5, chars=string.ascii_uppercase + string.digits)
            today_str = str(datetime.today().strftime('%Y%m%d-%H%M%S'))
            payment.reference_code = f"REF-{today_str}-{code}"
            payment.save()

        return payment
    