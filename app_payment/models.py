from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError


# Create your models here.
class Currency(models.Model):
    name = models.CharField(max_length=128)
    code = models.CharField(default='', max_length=128, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'
    
    def __str__(self):
        return self.name
    

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    reference_code = models.CharField(default='', max_length=128, unique=True)
    amount = models.FloatField()
    is_paid = models.BooleanField(default=False) 
    paid_date = models.DateField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reference_code} - {str(self.user)}"
    
    def check_user_payment_availability(self):
        today_payments = Payment.objects.filter(
            user=self.user,
            currency=self.currency,
            created_date__date=timezone.now().date()
        ).aggregate(total_amount=models.Sum('amount'))['total_amount'] or 0
        if today_payments + self.amount > 5000:
            return False, f"Amount limit exceeded. You can only create transactions up to {5000 - today_payments} {self.currency} currency today."
        return True, "Valid"
