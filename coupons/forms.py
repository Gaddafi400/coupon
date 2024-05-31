from django import forms
from coupons.models import Coupon


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
