from typing import List

from app import settings
from .models import UserProfile, User_Filter, Listing_Parameters, Listing
from django.core.mail import send_mail


# forcing default values on save if they are not set
# TODO: figure out how to set them as default without overwriting the placeholders
def min_max_beds_baths_init_set(user_filter: User_Filter):
    # forcing default values on save if they are not set
    user_filter.min_beds = user_filter.min_beds or 0
    user_filter.max_beds = user_filter.max_beds or 0
    user_filter.min_baths = user_filter.min_baths or 0
    user_filter.max_baths = user_filter.max_baths or 0

    # If the user doesn't select a max value, set it to -1 to allow for any number of beds/baths
    # Do not filter on max beds/baths if the user doesn't select a max value
    if user_filter.min_beds > user_filter.max_beds:
        user_filter.max_beds = None

    if user_filter.min_baths > user_filter.max_baths:
        user_filter.max_baths = None
    


def getUserFilter(user: UserProfile):
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=user)


    try:
        user_filter = user_profile.filter
    except User_Filter.DoesNotExist:
        user_filter = User_Filter()
    
    return user_filter



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

def match_gender(user_filter, listing_parameters):
    user_genders = set(user_filter.gender.values_list('id', flat=True))
    listing_genders = set(listing_parameters.gender.values_list('id', flat=True))

    # Check for intersection
    if user_genders.intersection(listing_genders):
        return True

    
    return False


def matches_user_filter(user_filter: User_Filter, listing_parameters: Listing_Parameters):
    return (
        (user_filter.price_limit >= listing_parameters.price or user_filter.price_limit is None or user_filter.no_price_limit) and
        (user_filter.min_beds <= listing_parameters.num_beds) and
        (not user_filter.max_beds or (user_filter.max_beds >= listing_parameters.num_beds)) and 
        (user_filter.min_baths <= listing_parameters.num_baths) and
        (not user_filter.max_baths or (user_filter.max_baths >= listing_parameters.num_baths)) and 
        ((user_filter.move_in_date >= listing_parameters.move_in_date) or (user_filter.move_in_date is None)) and
        ((user_filter.length_of_stay is None) or (set(user_filter.length_of_stay.values_list('id', flat=True)).intersection(set(listing_parameters.length_of_stay.values_list('id', flat=True))))) and
        (not user_filter.gender.all() or (set(user_filter.gender.values_list('id', flat=True))).intersection(set(listing_parameters.gender.values_list('id', flat=True)))) and
        (not user_filter.furnished or (user_filter.furnished and listing_parameters.furnished)) and
        (not user_filter.personal_bathroom or (user_filter.personal_bathroom and listing_parameters.personal_bathroom)) and
        (not user_filter.full_place or (user_filter.full_place and listing_parameters.full_place)) and
        (listing_parameters.neighbourhood in user_filter.neighbourhoods.all())
    )   

def send_aggregated_newsletter(user_email: str, listings: List[Listing]):
    # Placeholder function for sending an email with all matched listings
    # Implement your actual sending logic here, such as using Django's email functionality
    content = ""
    for listing in listings: 
        content += listing.title + " - " + listing.link + " - " + "available " + listing.parameters.move_in_date.strftime('%m/%d/%Y') + "\n"
    send_mail(    
            "New rentals available",
            content,
            settings.DEFAULT_FROM_EMAIL,
            [user_email],
            fail_silently=False,)
    listings_titles = [listing.title for listing in listings]
    print(f"Sending aggregated listings {listings_titles} to {user_email}")