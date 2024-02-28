from django.http import HttpResponse
from django.template import loader
from .models import UserProfile, Filter
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import FilterForm
from django.contrib.auth.forms import UserCreationForm


def index(request):
    return render(request, 'newsletter/index.html', {"form": UserCreationForm()})


def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Registration Successfull!"))
            return redirect('newsletter:profile')



def logout_user(request):
    pass

def login_user(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('newsletter:profile')
        else:
            messages.success(request, ("There was an error loggin in, try again..."))
            return redirect('newsletter:profile')
    
    return HttpResponse("Error")

def profile(request):
    if not request.user.is_authenticated:
        return HttpResponse(loader.get_template("newsletter/login.html").render({}, request))
    
    user_profile = UserProfile.objects.get(user=request.user)

    try:
        user_filter = user_profile.filter
    except Filter.DoesNotExist:
        user_filter = Filter()

    if request.method == 'POST':
        form = FilterForm(request.POST, instance=user_filter)
        if form.is_valid():
            # This line saves the Filter instance and associates it with the user profile
            user_profile.filter = form.save()
            user_profile.save()
            return redirect('newsletter:profile')  # Redirect to the profile page
    else:
        form = FilterForm(instance=user_filter)

    listings = user_profile.listings.all()
    
    template = loader.get_template("newsletter/profile.html")
    context = {
        "listings": listings,
        "form": form,
    }
    return HttpResponse(template.render(context, request))
