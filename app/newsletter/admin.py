from django.contrib import admin

from .models import Filter, Listing, UserProfile, Neighbourhood

admin.site.register(Listing)
admin.site.register(UserProfile)
admin.site.register(Filter)
admin.site.register(Neighbourhood)