from .models import UserProfile, Filter

def getUserFilter(user: UserProfile):
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=user)


    try:
        user_filter = user_profile.filter
    except Filter.DoesNotExist:
        user_filter = Filter()
    
    return user_filter