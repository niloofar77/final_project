from django.shortcuts import render, redirect,get_object_or_404
from .forms import UserLoginForm, UserRegistrationForm,EditProfileForm,ContactForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User, Profile,Contact
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, get_connection
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
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
	return render(request, 'accounts/login2.html', {'form':form})


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
				# full_name = form.cleaned_data['full_name']
				email = form.cleaned_data['email']
				message = form.cleaned_data['message']
				try:
					send_mail(subject, email, message, ['sn.mousavi77@gmail.com'])
				except BadHeaderError:
					return HttpResponse('Invalid header found.')
			messages.success(request, 'your profile edited successfully', 'success')
	else:
		form = ContactForm()
	return render(request, 'accounts/contact2.html', {'form':form})

def forget_Password(request):
	return render(request, 'accounts/forget_password.html')
