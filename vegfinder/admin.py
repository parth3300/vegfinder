from django.contrib import admin
from .models import Restaurant, Review
from .models import Restaurant, Review, City, State, Country


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    ordering = ['id']
    list_per_page = 10


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'country']
    list_filter = ['country']
    list_per_page = 10
    ordering = ['id']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'state']
    list_per_page = 10
    list_filter = ['state']
    ordering = ['id']
    search_fields = ['state']


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category',
                    'images', 'block_no', 'street', 'city', 'state', 'country', 'pincode', 'contact', 'ratings']

    list_per_page = 10
    list_filter = ['id', "city", "state", "country"]


@admin.register(Review)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'restaurant',
                    'description', 'ratings', 'date']
    ordering = ['id']
    list_per_page = 10
