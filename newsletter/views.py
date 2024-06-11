from django.http import HttpResponse
from members.models import CustomUser
from .models import UserProfile, User_Filter, Listing, Neighbourhood
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import FilterForm
from django.contrib.auth.forms import UserCreationForm

from django.utils.timezone import now, timedelta
from django.core.mail import send_mail

from django.utils import timezone


from .helpers import get_matching_listings, matches_user_filter, min_max_beds_baths_init_set, send_aggregated_newsletter

import json

from collections import defaultdict


def home(request):
    return render(request, 'home.html', {"form": UserCreationForm()})

def filters(request):
    # Redirect unauthenticated users
    if not request.user.is_authenticated:
        return redirect('members:login_user')
    
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if user_profile.filter:
        user_filter = user_profile.filter
        created = False
    else:
        # Create a new User_Filter instance and associate it with the UserProfile
        user_filter = User_Filter.objects.create()
        user_profile.filter = user_filter
        user_profile.save()
        created = True


    # user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    # user_filter: User_Filter = getattr(user_profile, 'filter', None)
    # user_filter, created = User_Filter.objects.get_or_create(userprofile=user_profile)



    if request.method == 'POST':
        form = FilterForm(request.POST, instance=user_filter)
        if form.is_valid():
            if not created:
                # If an existing filter was found, delete any other filters this user might have.
                User_Filter.objects.filter(userprofile=user_profile).exclude(pk=user_filter.pk).delete()

            user_filter = form.save(commit=False)
            form.save_m2m()  # Needed for saving ManyToMany fields if commit=False
            
            # forcing default values on save if they are not set
            # TODO: figure out how to set them as default without overwriting the placeholders
            min_max_beds_baths_init_set(user_filter)

            user_filter.save()

            user_profile.filter = user_filter
            user_profile.save()
            
            
            messages.success(request, "Filter Updated!")
            return redirect('newsletter:filters')
        else:
            messages.error(request, "Something went wrong with the form...")  # Use messages.error for errors
    else:
        form = FilterForm(instance=user_filter)

    user_neighbourhoods = list(user_filter.neighbourhoods.values('id', 'name')) if user_filter else []
    context = {
        "form": form,
        "all_neighbourhoods": Neighbourhood.objects.all(),
        "user_neighbourhoods": json.dumps(user_neighbourhoods),
        "user_price_limit": json.dumps(user_filter.price_limit if user_filter else 0),
    }

    if request.is_mobile:
        return render(request, "newsletter/mobile/mobile_filter.html", context)
    return render(request, "newsletter/filters.html", context)

def listings(request):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    user_filter = getattr(user_profile, 'filter', None)

    # Default to 'month' if 'timeframe' is not specified in the GET request
    selected_timeframe = request.GET.get('timeframe', 'month')
    
    # Define the timedelta for each timeframe
    delta = {
        'day': timedelta(days=1),
        'week': timedelta(weeks=1),
        'month': timedelta(days=30)
    }

    # Filter listings based on the selected timeframe
    if selected_timeframe in delta:
        time_threshold = now() - delta[selected_timeframe]
        listings = get_matching_listings(user_filter, Listing.objects.filter(pub_date__gte=time_threshold))
    else:
        listings = Listing.objects.all()

    # Pass the selected timeframe to the template via context
    context = {
        'listings': listings,
        'selected_timeframe': selected_timeframe
    }
    return render(request, 'newsletter/listings.html', context)

def settings(request):
    return render(request, 'newsletter/settings.html')

from django.contrib.auth.decorators import login_required, user_passes_test

def is_admin_user(user):
    return user.is_authenticated and user.is_superuser

@login_required
@user_passes_test(is_admin_user)
def send_aggregated_daily_newsletters(request):
    # Step 1: Fetch Listings from the past 24 hours
    yesterday = timezone.now() - timedelta(days=1)
    recent_listings = Listing.objects.filter(pub_date__gte=yesterday)

    all_listings = Listing.objects.all()
    # Initialize a dictionary to hold matching listings for each user
    user_listings_map = defaultdict(list)

    # Iterate through each user profile instead of each listing
    user_profiles = UserProfile.objects.all()
    for user_profile in user_profiles:
        for listing in all_listings:
            if matches_user_filter(user_profile.filter, listing.parameters):
                user_listings_map[user_profile.user.email].append(listing)

    # Step 2: Send a single Newsletter to each user with all matching listings
    print(user_profiles)
    for user_email, listings in user_listings_map.items():
        send_aggregated_newsletter(user_email, listings)
    
    return HttpResponse("Emails sent successfully")
