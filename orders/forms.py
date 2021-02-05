from django import forms


class CouponForm(forms.Form):
	code = forms.CharField(label="کد تخفیف ",label_suffix='')