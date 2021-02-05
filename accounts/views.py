from django.shortcuts import render, redirect,get_object_or_404
from .forms import UserLoginForm, UserRegistrationForm,EditProfileForm,ContactForm,PhoneLoginForm,VerifyCodeForm
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.contrib import messages
from .models import User, Profile,Contact,FAQ
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, get_connection
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import PasswordChangeForm
from random import randint
from kavenegar import *
def user_login(request):
	if request.method == 'POST':
		form = UserLoginForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = authenticate(request, email=cd['email'], password=cd['password'])
			if user is not None:
				login(request, user)
				messages.success(request, 'you logged in successfully', 'success')
				return redirect('shop:home')
			else:
				messages.error(request, 'username or password is wrong', 'danger')
	else:
		form = UserLoginForm()
	return render(request, 'accounts/login.html', {'form':form})


def user_logout(request):
	logout(request)
	messages.success(request, 'you logged out successfully', 'success')
	return redirect('shop:home')


def user_register(request):
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			user = User.objects.create_user(cd['email'], cd['full_name'], cd['password'])
			user.save()
			profile = Profile.objects.create( user = user)
			profile.save()

			messages.success(request, 'you registered successfully', 'success')
			return redirect('shop:home')
	else:
		form = UserRegistrationForm()
	return render(request, 'accounts/register.html', {'form':form})

def view_profile(request, pk=None):
	user_res = request.user
	profile = Profile.objects.get(user = user_res)
	return render(request, 'accounts/profile.html', {'profile':profile})

@login_required
def edit_profile(request):
	print('asss')
	user = Profile.objects.get(user = request.user)
	if request.method == 'POST':
		form = EditProfileForm(request.POST, instance=user)
		if form.is_valid():
			form.save()
			# user.email = form.cleaned_data['email']
			user.save()
			messages.success(request, 'your profile edited successfully', 'success')
		return render(request, 'accounts/edit_profile.html' , {'form':form})
	else:
		if user is  None:
			print('aaa')
			new_profile = Profile.objects.create(user = request.user )
			new_profile.save()
		else:
			form = EditProfileForm(instance= user, initial={'email':request.user.email})
	return render(request, 'accounts/edit_profile.html', {'form':form})
@login_required
def show_account(request):
	return render(request, 'accounts/my-account.html')
def contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			if form.is_valid():
				subject = form.cleaned_data['subject']
				full_name = form.cleaned_data['full_name']
				email = form.cleaned_data['email']
				message = form.cleaned_data['message']
				try:
					send_mail(subject, message, email, ['sn.mousavi77@gmail.com'])
					form= ContactForm()
				except BadHeaderError:
					return HttpResponse('Invalid header found.')
			messages.success(request, 'message sent!', 'success')
	else:
		form = ContactForm()
	return render(request, 'accounts/contact2.html', {'form':form})

def user_password(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			if form.is_valid():
				user = form.save()
				update_session_auth_hash(request, user)  # Important!
				messages.success(request, 'Your password was successfully updated!')
				return redirect('shop:home')
			else:
				messages.error(request, 'Please correct the error below.<br>' + str(form.errors))
				return redirect('accounts:user_password')
	else:
		form = PasswordChangeForm(request.user)
		return render(request, 'accounts/password_reset.html', {'form': form,  # 'category': category
													  })

def faq(request):
	# print('pppp')
	faq = FAQ.objects.filter(status="True").order_by("ordernumber")
	# print(faq)
	return render(request, 'accounts/faq.html',  {'faq':faq})
def phone_login(request):
	if request.method == 'POST':
		form = PhoneLoginForm(request.POST)
		if form.is_valid():
			phone = f"0{form.cleaned_data['phone']}"
			print(phone)
			rand_num = randint(1000, 9999)
			print(rand_num)
			api = KavenegarAPI('4861426E45445030577A62306A422F74354D5778443554382F72694747473556')
			params = {
				'receptor': phone,
				'template': 'verifyuser',
				'token': rand_num,
				'type': 'sms',  # sms vs call
			}
			response = api.verify_lookup(params)
			return redirect('accounts:verify', phone, rand_num)
	else:
		form = PhoneLoginForm()
	return render(request, 'accounts/phone_login.html', {'form':form})
def verify(request, phone, rand_num):
	if request.method == 'POST':
		form = VerifyCodeForm(request.POST)
		if form.is_valid():
			if rand_num == form.cleaned_data['code']:
				profile = get_object_or_404(Profile, phone=phone)
				user = get_object_or_404(User, profile__id=profile.id)
				login(request, user)
				messages.success(request, 'logged in successfully', 'success')
				return redirect('shop:home')
			else:
				messages.error(request, 'your code is wrong', 'warning')
	else:
		form = VerifyCodeForm()
	return render(request, 'accounts/verifyuser.html', {'form':form})