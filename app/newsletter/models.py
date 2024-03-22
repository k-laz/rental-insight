from django.db import models
from members.models import CustomUser
from datetime import date

class Neighbourhood(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Filter(models.Model):
    max_price = models.IntegerField(default=0)
    personal_bathroom = models.BooleanField(default=False)
    full_place = models.BooleanField(default=False)
    furnished = models.BooleanField(default=False)
    min_beds = models.IntegerField(default=0)
    min_bathrooms = models.IntegerField(default=0)

    # # if move_in_date is negotiable set to null and filter null as acceptable
    # move_in_date = models.DateField(default=date.today, null=True)
    # class LengthOfStayChoices(models.IntegerChoices):
    #     FOUR_MONTHS = 4, '4 months'
    #     EIGHT_MONTHS = 8, '8 months'
    #     TWELVE_MONTHS = 12, '12 months'
    #  # if length_of_stay is negotiable set to null and filter null as acceptable
    # length_of_stay = models.IntegerField(choices=LengthOfStayChoices.choices, default=LengthOfStayChoices.FOUR_MONTHS, null=True)

    class Gender(models.IntegerChoices):
        MALE = 0, 'male'
        FEMALE = 1, 'female'
        EITHER = 2, 'either'
    gender = models.IntegerField(choices=Gender.choices, default=Gender.EITHER)

    neighbourhoods = models.ManyToManyField(Neighbourhood, blank=True)



class Listing(models.Model):
    title = models.CharField(max_length=50)
    pub_date = models.DateTimeField("date published")
    link = models.CharField(max_length=200, null=True) 
    potential_spam = models.BooleanField(default=False)
    parameters = models.OneToOneField(Filter, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    listings = models.ManyToManyField(Listing, blank=True)
    filter = models.OneToOneField(
        Filter,
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        # Use the email field for the string representation
        return self.user.email
    
