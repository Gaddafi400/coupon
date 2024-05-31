from django import forms
from coupons.models import Coupon, Category


class CouponSearchForm(forms.Form):
    code = forms.CharField(max_length=50)


class CouponApplyForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code', 'customer_names', 'customer_phone', 'amount']
        widgets = {
            'code': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.required = True
            field.error_messages = {
                'required': f'{field.label} is required'
            }


class BulkCouponGenerationForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    count = forms.IntegerField(min_value=1)
    discount_amount = forms.DecimalField(max_digits=10, decimal_places=2)
    valid_from = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    valid_to = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))