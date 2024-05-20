from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import CustomUser
from newsletter.models import UserProfile
from .forms import RegisterUserForm

from .tokens import account_activation_token
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string

from django.contrib.auth.models import User
from django.http import HttpResponse


def delete_user(request):
    if request.method == "POST":
        print("deleting user")
        return redirect('newsletter:filters')
    return render(request, 'members/delete_user.html', {})


def login_user(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('newsletter:filters')
        else:
            messages.success(request, ("There Was An Error Logging In, Try Again..."))	
            return redirect('members:login_user')	
    else:
        return render(request, 'members/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, ("You Were Logged Out!"))
    return redirect('newsletter:filters')



def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(username=email, password=password)
            user.is_active = False
            user.save()
            # login(request, user)
            # messages.success(request, ("Registration Successful!"))
            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            send_mail(
                subject,
                message,
                "from@example.com",
                [email],
                fail_silently=False,
            )

            return render(request, 'members/message_page.html', {"msg": "Confirmation required: we sent an email to klazarevdev@gmail.com. Click the link there to finish subscribing"})
        else:
            messages.success(request, ("There was an error signing up, Try Again..."))	
            return redirect('members:register_user')	

    return render(request, 'members/register_user.html', {'form':RegisterUserForm()})



def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('newsletter:filters')
    else:
        # Invalid link or token
        return HttpResponse('Activation link is invalid!')
    

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
                return redirect("newsletter:filters")
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