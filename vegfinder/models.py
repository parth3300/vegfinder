from typing import Any
from django.db import models
from django.contrib.auth.models import User


class Country(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=50)
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name='states')

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=50)
    state = models.ForeignKey(
        State, on_delete=models.CASCADE, related_name='cities')

    def __str__(self):
        return self.name


class Owner(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='owners'
    )
    profile_pic = models.ImageField(upload_to='store/images')
    contact = models.BigIntegerField()

    def __str__(self) -> str:
        return str(self.user)


class UserProfile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE, related_name='userprofile',null=True)
    auth_token = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user.username


class OwnerProfile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,related_name='ownerprofile', null=True)
    profile_pic = models.ImageField(upload_to='vegfinder/images')
    auth_token = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.user.username


class Dharmshala(models.Model):
    user_name = models.ForeignKey(UserProfile,
                                  on_delete=models.CASCADE, null=True, blank=True)
    owner = models.ForeignKey(
        Owner, on_delete=models.CASCADE, related_name='dharmshala')
    title = models.CharField(max_length=100)
    images = models.ImageField(upload_to='vegfinder/images')
    block_no = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name='dharmshala_in_city')
    state = models.ForeignKey(
        State, on_delete=models.CASCADE, related_name='dharmshala_in_state')
    pincode = models.IntegerField()
    rooms = models.BigIntegerField()
    facilties = models.TextField()
    rent = models.BigIntegerField()
    restriction = models.TextField()
    contact = models.BigIntegerField()

    def __str__(self) -> str:
        return self.title


class Restaurant(models.Model):
    RATING_CHOICES = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]

    user_name = models.ForeignKey(UserProfile,
                                  on_delete=models.CASCADE, null=True, blank=True)
    owner = models.ForeignKey(
        Owner, on_delete=models.CASCADE, related_name='restaurants')
    title = models.CharField(max_length=100)
    images = models.ImageField(upload_to='vegfinder/images')
    block_no = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name='restaurants_in_city')
    state = models.ForeignKey(
        State, on_delete=models.CASCADE, related_name='restaurants_in_state')
    pincode = models.IntegerField()
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name='restaurants_in_country')
    contact = models.BigIntegerField()
    ratings = models.IntegerField(choices=RATING_CHOICES)

    def __str__(self) -> str:
        return self.title


class Hotel(models.Model):
    RATING_CHOICES = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]

    user_name = models.ForeignKey(UserProfile,
                                  on_delete=models.CASCADE, null=True, blank=True)
    owner = models.ForeignKey(
        Owner, on_delete=models.CASCADE, related_name='hotels')
    title = models.CharField(max_length=100)
    images = models.ImageField(upload_to='vegfinder/images')
    block_no = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.ForeignKey(
        City, on_delete=models.CASCADE, related_name='hotels_in_city')
    state = models.ForeignKey(
        State, on_delete=models.CASCADE, related_name='hotels_in_state')
    pincode = models.IntegerField()
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name='hotels_in_country')
    rent = models.BigIntegerField()
    contact = models.BigIntegerField()
    ratings = models.IntegerField(choices=RATING_CHOICES)

    def __str__(self) -> str:
        return self.title


class Review(models.Model):
    RATING_CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5')
    ]
    user = models.ForeignKey(UserProfile,
                             on_delete=models.CASCADE)
    dharmshala = models.ForeignKey(
        Dharmshala, on_delete=models.CASCADE, related_name='reviews_dharmshala', blank=None, null=True)
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name='reviews_restaurant', blank=None, null=True)
    hotel = models.ForeignKey(
        Hotel, on_delete=models.CASCADE, related_name='reviews_hotel', blank=None, null=True)

    description = models.TextField()
    ratings = models.CharField(max_length=1, choices=RATING_CHOICES)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.ratings
