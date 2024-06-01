from django import forms
from coupons.models import Coupon, Category
from django.contrib.admin.widgets import AdminDateWidget


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
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        label="Category",
        help_text="Select the category for the coupons.",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    count = forms.IntegerField(
        min_value=1,
        label="Number of Coupons",
        help_text="Enter the number of coupons to generate.",
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        error_messages={
            'min_value': "The number of coupons must be at least 1.",
            'invalid': "Enter a valid number."
        }
    )
    discount_amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label="Discount Amount",
        help_text="Enter the discount amount for each coupon.",
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        error_messages={
            'invalid': "Enter a valid discount amount."
        }
    )
    valid_from = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'custom-date-style'}),
        label="Valid From",
        help_text="The date from which the coupons are valid.",
        error_messages={
            'invalid': "Enter a valid date."
        }
    )
    valid_to = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'custom-date-style'}),
        label="Valid To",
        help_text="The date until which the coupons are valid.",
        error_messages={
            'invalid': "Enter a valid date."
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        valid_from = cleaned_data.get("valid_from")
        valid_to = cleaned_data.get("valid_to")

        if valid_from and valid_to and valid_from > valid_to:
            raise forms.ValidationError("The 'Valid From' date cannot be after the 'Valid To' date.")

        return cleaned_data
