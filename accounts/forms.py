from django import forms
from .models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import Profile
from django import forms
from captcha.fields import CaptchaField

class UserCreationForm(forms.ModelForm):
	password1 = forms.CharField(label='password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('email', 'full_name')

	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
			raise forms.ValidationError('passwords must match')
		return cd['password2']

	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user


class UserChangeForm(forms.ModelForm):
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = User
		fields = ('email', 'password', 'full_name')

	def clean_password(self):
		return self.initial['password']


class UserLoginForm(forms.Form):
	email = forms.EmailField(label="ایمیل",label_suffix='',widget=forms.EmailInput(attrs={'class':'form-control'}))
	password = forms.CharField(label="رمز عبور",label_suffix='',widget=forms.PasswordInput(attrs={'class':'form-control'}))


class UserRegistrationForm(forms.Form):
	email = forms.EmailField(label="ایمیل",label_suffix='',widget=forms.EmailInput(attrs={'class': 'form-control'}))
	full_name = forms.CharField(label="نام و نام خانوادگی",label_suffix='',widget=forms.TextInput(attrs={'class':'form-control'}))
	password = forms.CharField(label="رمز عبور",label_suffix='',widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	captcha = CaptchaField(label="",label_suffix='')

class ContactForm(forms.Form):
	full_name = forms.CharField(label="نام و نام خانوادگی",label_suffix='',widget=forms.TextInput(attrs={'class':'form-control'}))
	email = forms.EmailField(label="ایمیل",label_suffix='',required=True,widget=forms.EmailInput(attrs={'class': 'form-control'}))
	subject = forms.CharField(label="موضوع",label_suffix='',required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
	message = forms.CharField(label="متن پیام",label_suffix='',widget=forms.Textarea(attrs={'class':'form-control'}))

class EditProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('bio', 'age','phone')
		labels = {
			'bio': ('بیو'),
			'age':('سن'),
			'phone':('تلفن')
		}



class PhoneLoginForm(forms.Form):
	phone = forms.IntegerField(label="تلفن",label_suffix='')

	def clean_phone(self):
		phone = Profile.objects.filter(phone=self.cleaned_data['phone'])
		if not phone.exists():
			raise forms.ValidationError('This phone number does not exists')
		return self.cleaned_data['phone']


class VerifyCodeForm(forms.Form):
	code = forms.IntegerField(label="کد",label_suffix='')


