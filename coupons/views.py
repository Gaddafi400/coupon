from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils import timezone
from .forms import CouponApplyForm
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404, redirect
from .models import Coupon
from .forms import CouponSearchForm
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def search_coupon(request):
    coupon = None
    if request.method == 'POST':
        form = CouponSearchForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code=code)
            except Coupon.DoesNotExist:
                form.add_error('code', 'This coupon does not exist.')
    else:
        form = CouponSearchForm()
    now = timezone.now()
    return render(request, 'coupons/search_coupon.html', {'form': form, 'coupon': coupon, 'now': now})


@login_required
def apply_coupon(request):
    final_amount = None
    code = request.GET.get('code', None)
    coupon = None
    if code:
        coupon = get_object_or_404(Coupon, code=code)
    else:
        return redirect('search_coupon')
    if request.method == 'POST':
        form = CouponApplyForm(request.POST, instance=coupon)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            now = timezone.now()
            if coupon and coupon.valid_from <= now <= coupon.valid_to and coupon.active:
                # Update coupon details
                coupon.customer_names = form.cleaned_data['customer_names']
                coupon.customer_phone = form.cleaned_data['customer_phone']
                coupon.amount = amount
                coupon.updated_by = request.user
                if not coupon.created_by:
                    coupon.created_by = request.user
                coupon.active = False  # Expire the coupon after applying
                coupon.save()
                final_amount = coupon.total_amount_after_discount
                messages.success(request,
                                 f'Coupon applied successfully. The final amount after discount is {final_amount:.2f}.')
                return redirect('search_coupon')  # Redirect to search coupon page
            else:
                form.add_error('code', 'This coupon is not valid.')
    else:
        form = CouponApplyForm(instance=coupon)

    return render(request, 'coupons/apply_coupon.html', {'form': form, 'final_amount': final_amount})