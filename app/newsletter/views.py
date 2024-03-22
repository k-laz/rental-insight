from django.http import HttpResponse
from django.template import loader
from .helpers import getUserFilter

from members.models import CustomUser
from .models import UserProfile, Filter, Listing, Neighbourhood
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import FilterForm
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.utils.timezone import now, timedelta

from django.urls import reverse

import json


def home(request):
    return render(request, 'home.html', {"form": UserCreationForm()})

def filters(request):
    # Redirect unauthenticated users
    if not request.user.is_authenticated:
        return redirect('members:login_user')
    
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    user_filter = getattr(user_profile, 'filter', None)

    if request.method == 'POST':
        form = FilterForm(request.POST, instance=user_filter)
        if form.is_valid():
            # Save Filter instance and potentially associate with UserProfile
            user_filter = form.save(commit=False)
            user_filter.user_profile = user_profile
            user_filter.save()
            form.save_m2m()  # Needed for saving ManyToMany fields if commit=False
            
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
    }

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



# return a list of listings that matches the given filter (past month, past week, today)
def get_matching_listings(search_filter, listings):
    """
    Returns listings that match the given filter criteria.
    :param search_filter: An instance of the Filter model containing search criteria.
    :return: A queryset of Listing instances matching the search criteria.
    """
    res = []
    for listing in listings:
        if matches_user_filter(search_filter, listing.parameters):
            res.append(listing)

    return res


from django.core.mail import send_mail
def send_email(request):
    users = CustomUser.objects.all()

    for user in users:
        listings = UserProfile.objects.get(user=user).listings.all()
        content = ""
        for listing in listings: 
            content += listing.title + " " + listing.link

        send_mail(    
            "Test email",
            content,
            "from@example.com",
            ["to@example.com"],
            fail_silently=False,)
    return HttpResponse("sent!")
    #send_mass_mail((message1, message2), fail_silently=False)


from collections import defaultdict
def send_aggregated_daily_newsletters(request):
    # Step 1: Fetch Listings from the past 24 hours
    yesterday = timezone.now() - timedelta(days=1)
    recent_listings = Listing.objects.filter(pub_date__gte=yesterday)

    # Initialize a dictionary to hold matching listings for each user
    user_listings_map = defaultdict(list)

    # Iterate through each user profile instead of each listing
    user_profiles = UserProfile.objects.all()
    for user_profile in user_profiles:
        for listing in recent_listings:
            if matches_user_filter(user_profile.filter, listing.parameters):
                user_listings_map[user_profile.user.email].append(listing)

    # Step 2: Send a single Newsletter to each user with all matching listings
    for user_email, listings in user_listings_map.items():
        send_aggregated_newsletter(user_email, listings)
    
    return HttpResponse("done")

def matches_user_filter(user_filter: Filter, listing_parameters: Filter):
    # Implement the logic to check if a listing's parameters match the user's filter
    # This is a simplified check; adjust according to your filter fields and requirements
    preferred_neighborhood_ids = user_filter.neighbourhoods.values_list('id', flat=True)

    return (
        (user_filter.max_price >= listing_parameters.max_price) and
        (not user_filter.personal_bathroom or (user_filter.personal_bathroom and listing_parameters.personal_bathroom)) and
        (user_filter.min_beds <= listing_parameters.min_beds) and
        (user_filter.min_bathrooms <= listing_parameters.min_bathrooms) and
        # Figure out dates (when is move in appropriate ?) this seems to be increadibly negotiable
        #((user_filter.move_in_date >= listing_parameters.move_in_date) or (user_filter.move_in_date is None)) and
        #((user_filter.length_of_stay <= listing_parameters.length_of_stay) or (user_filter.length_of_stay is None)) and
        ((user_filter.gender == listing_parameters.gender) or user_filter.gender == "either") and
        (user_filter.furnished == listing_parameters.furnished or (not user_filter.furnished)) and
        (listing_parameters.neighbourhoods.all() in user_filter.neighbourhoods.all())
    )

def send_aggregated_newsletter(user_email, listings):
    # Placeholder function for sending an email with all matched listings
    # Implement your actual sending logic here, such as using Django's email functionality
    content = ""
    for listing in listings: 
        content += listing.title + " - " + listing.link + " - " + "available " + listing.parameters.move_in_date.strftime('%m/%d/%Y') + "\n"

    send_mail(    
            "New rentals available",
            content,
            "from@example.com",
            [user_email],
            fail_silently=False,)
    listings_titles = [listing.title for listing in listings]
    print(f"Sending aggregated listings {listings_titles} to {user_email}")

# This function sends an aggregated email to each user with all listings that matched their filter.
# You would replace the print statement in send_aggregated_newsletter with your actual email sending logic.




# def profile(request):
#     # Redirect unauthenticated users
#     if not request.user.is_authenticated:
#         return redirect('members:login_user')
    
#     user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
#     user_filter = getattr(user_profile, 'filter', None)

#     listings = []
#     user_neighbourhoods = []

#     if request.method == 'POST':
#         form = FilterForm(request.POST, instance=user_filter)
#         if form.is_valid():
#             # Save Filter instance and potentially associate with UserProfile
#             user_filter = form.save(commit=False)
#             user_filter.user_profile = user_profile
#             user_filter.save()
#             form.save_m2m()  # Needed for saving ManyToMany fields if commit=False
            
#             messages.success(request, "Filter Updated!")
#             return redirect('newsletter:profile')
#         else:
#             messages.error(request, "Something went wrong with the form...")  # Use messages.error for errors
#     else:
#         form = FilterForm(instance=user_filter)

#     if user_filter:
#         TIMEFRAMES = {'MONTH': 30, 'WEEK': 7, 'DAY': 1}
#         listings = get_matching_listings(user_filter, TIMEFRAMES['MONTH'])
#         user_neighbourhoods = list(user_filter.neighbourhoods.values('id', 'name'))

#     breadcrumbs = [
#         ('Filters', reverse('newsletter:filters')),
#         ('Listings', reverse('newsletter:listings')),
#         # Additional breadcrumbs as needed
#     ]

#     context = {
#         "listings": listings,
#         "form": form,
#         "neighbourhoods": Neighbourhood.objects.all(),
#         "user_hoods": json.dumps(user_neighbourhoods),
#         'breadcrumbs': breadcrumbs,
#     }

#     return render(request, "newsletter/profile.html", context)