from django.db import models
from django.contrib.auth.models import User


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)

    customer_names = models.CharField(max_length=255, null=True, blank=True)
    customer_phone = models.CharField(max_length=11, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_amount_after_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(User, related_name='coupons_created', on_delete=models.SET_NULL, null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name='coupons_updated', on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Only calculate total_amount_after_discount if both amount and discount are provided
        if self.amount is not None and self.discount is not None:
            self.total_amount_after_discount = self.amount - self.discount
        else:
            self.total_amount_after_discount = None
        super().save(*args, **kwargs)

    def __str__(self):
        name = 'empty'
        return f'{self.customer_names or name} - {self.code}'
