from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm

def login_user(request):
	if request.method == "POST":
		email = request.POST['email']
		password = request.POST['password']
		user = authenticate(request, username=email, password=password)
		if user is not None:
			login(request, user)
			return redirect('newsletter:profile')
		else:
			messages.success(request, ("There Was An Error Logging In, Try Again..."))	
			return redirect('members:login_user')	
	else:
		return render(request, 'members/login.html', {})


def logout_user(request):
	logout(request)
	messages.success(request, ("You Were Logged Out!"))
	return redirect('newsletter:profile')


def register_user(request):
	if request.method == "POST":
		form = RegisterUserForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data['email']
			password = form.cleaned_data['password1']
			user = authenticate(username=email, password=password)
			login(request, user)
			messages.success(request, ("Registration Successful!"))
			return redirect('newsletter:profile')

	return render(request, 'members/register_user.html', {'form':RegisterUserForm()})