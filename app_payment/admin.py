from django.contrib import admin
from app_payment.models import (
    Currency,
    Payment
)

# Register your models here.
@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin): 
    list_display = ('name', 'code', 'created_date')
    search_fields = ('name', 'code')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin): 
    raw_id_fields = ('user', 'currency')
    list_display = (
        'reference_code', 'user', 'currency', 'amount', 'is_paid', 'paid_date', 'created_date'
    )
    search_fields = (
        'reference_code', 
        'user__first_name', 
        'user__last_name', 
        'user__email'
    )
    list_filter = [
        'currency'
    ]