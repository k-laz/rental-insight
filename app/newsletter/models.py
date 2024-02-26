from django.db import models
from django.contrib.auth.models import User
from datetime import date



class Listing(models.Model):
    title = models.CharField(max_length=50)
    pub_date = models.DateTimeField("date published")
    link = models.CharField(max_length=200, null=True) 
    own_bathroom = models.BooleanField(default=False)
    beds = models.IntegerField(default=0)
    bathrooms = models.IntegerField(default=0)
    location = models.CharField(max_length=100, default="UBC campus")
    price = models.IntegerField(default=0)
    potential_spam = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Filter(models.Model):
    max_price = models.IntegerField(default=0)
    own_bathroom = models.BooleanField(default=False)
    min_beds = models.IntegerField(default=0)
    min_bathrooms = models.IntegerField(default=0)
    move_in_date = models.DateField(default=date.today)
    class LengthOfStayChoices(models.IntegerChoices):
        FOUR_MONTHS = 4, '4 months'
        EIGHT_MONTHS = 8, '8 months'
        TWELVE_MONTHS = 12, '12 months'
    length_of_stay = models.IntegerField(choices=LengthOfStayChoices.choices, default=LengthOfStayChoices.FOUR_MONTHS)

    class Gender(models.IntegerChoices):
        MALE = 0, 'male'
        FEMALE = 1, 'female'
    gender = models.IntegerField(choices=Gender.choices, default=Gender.MALE)



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    listings = models.ManyToManyField(Listing)
    filter = models.OneToOneField(
        Filter,
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self):
        return self.user.username