from django.shortcuts import render, redirect,get_object_or_404
from .forms import UserLoginForm, UserRegistrationForm,EditProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User
from django.contrib.auth.decorators import login_required

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
			messages.success(request, 'you registered successfully', 'success')
			return redirect('shop:home')
	else:
		form = UserRegistrationForm()
	return render(request, 'accounts/register.html', {'form':form})

def view_profile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user
    args = {'user': user}
    return render(request, 'accounts/profile.html', args)

@login_required
def edit_profile(request, user_id):
	user = get_object_or_404(User, id=user_id)
	if request.method == 'POST':
		form = EditProfileForm(request.POST, instance=user.profile)
		if form.is_valid():
			form.save()
			user.email = form.cleaned_data['email']
			user.save()
			messages.success(request, 'your profile edited successfully', 'success')
		return render(request, 'shop/test.html')
	else:
		form = EditProfileForm(instance=user.profile, initial={'email':request.user.email})
	return render(request, 'accounts/edit_profile.html', {'form':form})
@login_required
def show_account(request):
	return render(request, 'accounts/my-account.html')
