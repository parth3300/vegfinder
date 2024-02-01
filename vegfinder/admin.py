from django.contrib import admin
from .models import Restaurant, Review
from .models import Country, State, City, Owner, UserProfile, OwnerProfile, Dharmshala, Restaurant, Hotel, Review


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    ordering = ['id']


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'country', 'cities']
    list_filter = ['country']
    list_per_page = 10
    ordering = ['id']

    def cities(self, state):
        return [city for city in state.cities.all()]


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'state']
    list_filter = ['state']
    list_per_page = 10
    ordering = ['id']
    search_fields = ['state']


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'profile_pic', 'dharmshala_list',
                    'restaurants_list', 'hotels_list', 'contact']
    list_filter = ['user__username']
    ordering = ['id']

    def name(self, owner):
        return owner.user.username

    def dharmshala_list(self, owner):
        return [dharmshala.title for dharmshala in owner.dharmshala.all()]

    def restaurants_list(self, owner):
        return [restaurant.title for restaurant in owner.restaurants.all()]

    def hotels_list(self, owner):
        return [hotel.title for hotel in owner.hotels.all()]


@admin.register(Dharmshala)
class DharmshalaAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user_name', 'owner', 'images', 'block_no', 'street', 'city',
                    'state', 'pincode', 'rooms', 'facilties', 'rent', 'restriction', 'contact']
    list_filter = ["state"]
    list_per_page = 10
    ordering = ['id']


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user_name', 'owner',
                    'images', 'block_no', 'street', 'city', 'state', 'country', 'pincode', 'contact', 'ratings']
    list_filter = ["state", "country"]
    list_per_page = 10
    ordering = ['id']


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user_name', 'owner',
                    'images', 'block_no', 'street', 'city', 'state', 'country', 'pincode', 'contact', 'ratings']
    list_filter = ["state", "country"]
    list_per_page = 10
    ordering = ['id']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'dharmshala', 'restaurant', 'hotel',
                    'description', 'ratings', 'date']
    ordering = ['id']
    list_per_page = 10


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'auth_token', 'is_verified']
    ordering = ['id']


@admin.register(OwnerProfile)
class OwnerProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'auth_token', 'is_verified', 'profile_pic']
    ordering = ['id']
