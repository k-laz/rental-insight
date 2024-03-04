from django.http import HttpResponse
from django.template import loader

from members.models import CustomUser
from .models import UserProfile, Filter, Listing
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import FilterForm
from django.contrib.auth.forms import UserCreationForm


def index(request):
    return render(request, 'newsletter/index.html', {"form": UserCreationForm()})


def profile(request):
    if not request.user.is_authenticated:
        return redirect('members:login_user') 
    
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)


    try:
        user_filter = user_profile.filter
    except Filter.DoesNotExist:
        user_filter = Filter()

    if request.method == 'POST':
        form = FilterForm(request.POST, instance=user_filter)
        if form.is_valid():
            # This line saves the Filter instance and associates it with the user profile
            user_profile.filter = form.save()
            # TypeError Direct assignment to the forward side of a many-to-many set is prohibited. Use listings.set() instead.
            # user_profile.listings = get_matching_listings(user_profile.filter)
            user_profile.save()
            messages.success(request, ("Filter Updated!"))
            return redirect('newsletter:profile')  # Redirect to the profile page
        else:
            messages.success(request, ("Something went wrong with the form..."))
            return redirect('newsletter:profile')
    else:
        # get the form from user filter
        # TODO: figure out how to do it for multiple filters
        form = FilterForm(instance=user_filter)

    #listings = user_profile.listings.all()
    TIMEFRAMES = {
        'MONTH': 30,
        'WEEK': 7,
        'DAY': 1,
    }

    listings = get_matching_listings(user_filter, TIMEFRAMES['MONTH'])
    
    template = loader.get_template("newsletter/profile.html")
    context = {
        "listings": listings,
        "form": form,
        "user": user_profile.user,
    }
    return HttpResponse(template.render(context, request))

def register_filter(request):
    pass

def update_listings(user, filter):
    pass    

from django.utils import timezone
from datetime import timedelta

# return a list of listings that matches the given filter (past month, past week, today)
def get_matching_listings(search_filter, timeframe):
    """
    Returns listings that match the given filter criteria.
    :param search_filter: An instance of the Filter model containing search criteria.
    :return: A queryset of Listing instances matching the search criteria.
    """
    time_filter = timezone.now() - timedelta(days=timeframe)

    # listings = Listing.objects.all()
    listings = Listing.objects.filter(pub_date__gte=time_filter)

    
  
    # Problem: how do we filter by move in date when its very negotiable and uncertain ?
    # Solution right now: listing will match user if the move in date on the listing is earlier then move in date 
    # specified by the user IE: listing -> may 1, user -> may 2 = YES, but listing -> may 1, user -> april 1 = NO
    
    # Apply filters
    listings = listings.filter(parameters__max_price__lte=search_filter.max_price, parameters__personal_bathroom=search_filter.personal_bathroom, parameters__min_beds__gte=search_filter.min_beds, parameters__min_bathrooms__gte=search_filter.min_bathrooms, parameters__move_in_date__lte=search_filter.move_in_date, parameters__length_of_stay=search_filter.length_of_stay, parameters__gender=search_filter.gender)

    return listings
