from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Listing
from .tasks import send_listing_emails

# @receiver(post_save, sender=Listing)
# def listing_added(sender, instance, created, **kwargs):
#     if created:
#         send_listing_emails.delay(instance.id)
