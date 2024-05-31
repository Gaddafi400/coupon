from django.contrib import admin
from .models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount', 'valid_from', 'valid_to', 'active']
    search_fields = ['code']
    list_filter = ['active', 'valid_from', 'valid_to']
    # readonly_fields = ['code']
