from django.contrib import admin

from .models import User_Filter, Listing, UserProfile, Neighbourhood, Listing_Parameters, GenderOption, LengthOfStayOption

admin.site.register(Listing)
admin.site.register(UserProfile)
admin.site.register(User_Filter)
admin.site.register(Listing_Parameters)
admin.site.register(Neighbourhood)
admin.site.register(GenderOption)
admin.site.register(LengthOfStayOption)