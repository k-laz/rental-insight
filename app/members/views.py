from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import CustomUser
from newsletter.models import UserProfile
from .forms import RegisterUserForm


def delete_user(request):
    if request.method == "POST":
        print("deleting user")
        return redirect('newsletter:profile')
    return render(request, 'members/delete_user.html', {})


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
        else:
            messages.success(request, ("There was an error signing up, Try Again..."))	
            return redirect('members:register_user')	

    return render(request, 'members/register_user.html', {'form':RegisterUserForm()})


def change_password(request):
    if request.method == "POST":
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        
        try:
            user = CustomUser.objects.get(userprofile=UserProfile.objects.get(user=request.user))
            print(user.password)
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                messages.success(request, "Your password has been updated successfully.")
                return redirect("newsletter:profile")
            else:
                messages.error(request, "The old password is incorrect.")
                return render(request, 'members/change_password.html', {})  
        except CustomUser.DoesNotExist:
            messages.error(request, "User does not exist.")
            return render(request, 'members/change_password.html', {})  
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return render(request, 'members/change_password.html', {})
    else:
        # Handle the case for non-POST requests
        pass

    return render(request, 'members/change_password.html', {})

def reset_password(request):
    if request.method == "POST":
        email = request.POST.get('email')

    return render(request, 'members/reset_password.html', {})