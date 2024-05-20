from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Listing, UserProfile
from datetime import date

@shared_task
def send_listing_emails(listing_id):
    listing = Listing.objects.get(id=listing_id)
    listing_params = listing.parameters

    # Construct the query dynamically based on the listing's parameters
    query = {
        'filter__max_price__gte': listing_params.max_price,
        'filter__personal_bathroom': listing_params.personal_bathroom,
        'filter__min_beds__lte': listing_params.min_beds,
        'filter__min_bathrooms__lte': listing_params.min_bathrooms,
    }

    # For optional fields like move_in_date and length_of_stay, add them to the query if they are not null
    # if listing_params.move_in_date:
    #     query['filter__move_in_date__gte'] = listing_params.move_in_date
    # else:
    #     query['filter__move_in_date__isnull'] = True

    # if listing_params.length_of_stay:
    #     query['filter__length_of_stay__gte'] = listing_params.length_of_stay
    # else:
    #     query['filter__length_of_stay__isnull'] = True

    # Add gender to the query
    query['filter__gender'] = listing_params.gender

    # Filter UserProfiles based on constructed query
    matching_users = UserProfile.objects.filter(**query)

    # Send emails to users whose filters match the listing's parameters
    for user in matching_users:
        send_mail(
            'New Listing Available',
            f'Check out this new listing: {listing.title} : {listing.link}',
            settings.EMAIL_HOST_USER,
            [user.user.email],  # Assuming `user` has a `user` attribute that is a CustomUser instance
            fail_silently=False,
        )
