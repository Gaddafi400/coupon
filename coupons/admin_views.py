import random
import string
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import BulkCouponGenerationForm
from .models import Coupon

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
            
            coupons = []
            for _ in range(count):
                code = generate_random_code()
                coupons.append(Coupon(code=code, category=category, discount=discount_amount, valid_from=timezone.now(), valid_to=timezone.now() + timedelta(days=30)))
            
            Coupon.objects.bulk_create(coupons)
            messages.success(request, f'Successfully generated {count} coupons')
            return redirect('admin:bulk_generate_coupons')
    else:
        form = BulkCouponGenerationForm()
    
    return render(request, 'admin/coupons/bulk_generate_coupons.html', {'form': form})
