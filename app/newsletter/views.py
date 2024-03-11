from django.http import HttpResponse
from django.template import loader

from members.models import CustomUser
from .models import UserProfile, Filter, Listing, Neighbourhood
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import FilterForm
from django.contrib.auth.forms import UserCreationForm


def index(request):
    return render(request, 'index.html', {"form": UserCreationForm()})


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
    listings = get_matching_listings(user_filter, TIMEFRAMES['MONTH']) if user_filter else []
    
    template = loader.get_template("newsletter/profile.html")
    context = {
        "listings": listings,
        "form": form,
        "user": user_profile.user,
        "neighbourhoods": Neighbourhood.objects.all(),
    }
    return HttpResponse(template.render(context, request))



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
    listings = Listing.objects.filter(pub_date__gte=time_filter)

    listings = listings.filter(
        parameters__max_price__lte=search_filter.max_price,
        parameters__personal_bathroom=search_filter.personal_bathroom,
        parameters__min_beds__gte=search_filter.min_beds,
        parameters__min_bathrooms__gte=search_filter.min_bathrooms,
        parameters__gender=search_filter.gender,
        parameters__furnished=search_filter.furnished,
    )

    # Filter by neighbourhoods included in the user's filter
    # Assuming each listing is directly associated with a Neighbourhood
    # Or you can adjust this logic if the association is through the parameters field
    # user_neighbourhood_ids = search_filter.neighbourhoods.values_list('id', flat=True)
    # listings = listings.filter(neighbourhood__id__in=user_neighbourhood_ids)
    if search_filter.neighbourhoods.exists():  # Checking if there are any neighbourhoods selected in the filter
        listings = listings.filter(parameters__neighbourhoods__in=search_filter.neighbourhoods.all())

    
    return listings


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

def matches_user_filter(user_filter, listing_parameters):
    # Implement the logic to check if a listing's parameters match the user's filter
    # This is a simplified check; adjust according to your filter fields and requirements
    return (
        (user_filter.max_price >= listing_parameters.max_price) and
        (not user_filter.personal_bathroom or (user_filter.personal_bathroom and listing_parameters.personal_bathroom)) and
        (user_filter.min_beds <= listing_parameters.min_beds) and
        (user_filter.min_bathrooms <= listing_parameters.min_bathrooms) and
        # Figure out dates (when is move in appropriate ?) this seems to be increadibly negotiable
        ((user_filter.move_in_date <= listing_parameters.move_in_date) or (user_filter.move_in_date is None)) and
        ((user_filter.length_of_stay <= listing_parameters.length_of_stay) or (user_filter.length_of_stay is None)) and
        (user_filter.gender == listing_parameters.gender)
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
