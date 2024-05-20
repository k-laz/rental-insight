from django.db import models
from members.models import CustomUser
from datetime import date
from django.core.validators import MinValueValidator, MaxValueValidator


class Neighbourhood(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class LengthOfStayOption(models.Model):
    duration = models.IntegerField(unique=True)
    label = models.CharField(max_length=10)

    def __str__(self):
        return self.label

class GenderOption(models.Model):
    gender = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.gender
    

class User_Filter(models.Model):
    price_limit = models.IntegerField(
        default=None, null=True, blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(8100) 
        ]
    )
    no_price_limit = models.BooleanField(default=None, null=True, blank=True)

    personal_bathroom = models.BooleanField(default=False)
    full_place = models.BooleanField(default=False)
    furnished = models.BooleanField(default=False)
    min_beds = models.IntegerField(default=None, null=True, blank=True)
    max_beds = models.IntegerField(default=None, null=True, blank=True)
    min_baths = models.IntegerField(default=None, null=True, blank=True)
    max_baths = models.IntegerField(default=None, null=True, blank=True)
    
    move_in_date = models.DateField(default=None, null=True, blank=True)

    length_of_stay = models.ManyToManyField(LengthOfStayOption, blank=True)
    gender = models.ManyToManyField(GenderOption, blank=True)
    neighbourhoods = models.ManyToManyField(Neighbourhood, blank=True)

    def __str__(self):
        return f"USER=price:{self.price_limit} - beds:{self.min_beds} - baths:{self.min_baths} - furnished:{self.furnished} - full_place:{self.full_place} - personal_bath:{self.personal_bathroom} - gender:{self.gender.all()} - move_in:{self.move_in_date} - length_of_stay:{self.length_of_stay}"



class Listing_Parameters(models.Model):
    price = models.IntegerField(default=0)
    move_in_date = models.DateField(default=date.today)
    length_of_stay = models.ManyToManyField(LengthOfStayOption, blank=True)
    num_baths = models.IntegerField(default=0)
    num_beds = models.IntegerField(default=0) 
    furnished = models.BooleanField(default=False)
    full_place = models.BooleanField(default=False)
    personal_bathroom = models.BooleanField(default=False)
    gender = models.ManyToManyField(GenderOption, blank=True)
    neighbourhood = models.ForeignKey(Neighbourhood, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"LISTING=price:{self.price} - beds:{self.num_beds} - baths:{self.num_baths} - furnished:{self.furnished} - full_place:{self.full_place} - personal_bath:{self.personal_bathroom} - gender:{self.gender.all()} - hood:{self.neighbourhood}"
    

class Listing(models.Model):
    title = models.CharField(max_length=500)
    link = models.CharField(max_length=200, null=True) 
    potential_spam = models.BooleanField(default=False)
    pub_date = models.DateTimeField("date published", null=True)
    parameters = models.OneToOneField(Listing_Parameters, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    listings = models.ManyToManyField(Listing, blank=True)
    filter = models.OneToOneField(
        User_Filter,
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        # Use the email field for the string representation
        return self.user.email
    
