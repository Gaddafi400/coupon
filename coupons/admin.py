from django.contrib import admin
from django.urls import path, reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
import random
import string

from .models import Coupon, Category
from .forms import BulkCouponGenerationForm

def generate_random_code(length=8):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

def bulk_generate_coupons(request):
    if request.method == 'POST':
        form = BulkCouponGenerationForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category']
            count = form.cleaned_data['count']
            discount_amount = form.cleaned_data['discount_amount']
            valid_from = form.cleaned_data.get('valid_from', timezone.now())
            valid_to = form.cleaned_data.get('valid_to', timezone.now() + timedelta(days=30))

            coupons = []
            for _ in range(count):
                code = generate_random_code()
                coupons.append(Coupon(code=code, category=category, discount=discount_amount, valid_from=valid_from, valid_to=valid_to, active=True))

            Coupon.objects.bulk_create(coupons)
            messages.success(request, f'Successfully generated {count} coupons')
            return redirect('admin:coupons_coupon_changelist')
    else:
        form = BulkCouponGenerationForm()

    return render(request, 'admin/coupons/bulk_generate_coupons.html', {'form': form})

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'category', 'discount', 'valid_from', 'valid_to', 'active', 'customer_names', 'customer_phone', 'amount', 'total_amount_after_discount', 'created_at', 'updated_at']
    search_fields = ['code', 'customer_names', 'customer_phone']
    list_filter = ['category', 'active', 'valid_from', 'valid_to']
    readonly_fields = ['created_at', 'updated_at']
    change_list_template = 'admin/coupons/change_list.html'  # Use a custom change list template

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('bulk_generate/', self.admin_site.admin_view(bulk_generate_coupons), name='bulk_generate_coupons'),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['bulk_generate_url'] = reverse('admin:bulk_generate_coupons')
        return super().changelist_view(request, extra_context=extra_context)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
