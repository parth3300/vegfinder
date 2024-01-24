from rest_framework import serializers
from .models import Restaurant, Review


class RestaurantSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()

    def get_address(self, restaurant):
        return f'{restaurant.block_no} {restaurant.street} {restaurant.city} {restaurant.state} {restaurant.country} -{restaurant.pincode}'

    class Meta:
        model = Restaurant
        fields = ['id', 'title', 'category',
                  'images', 'address', 'contact', 'ratings']


class CustomRestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = ['id', 'title', 'category',
                  'images', 'block_no', 'street', 'city', 'state', 'country', 'pincode', 'contact', 'ratings']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'name', 'restaurant', 'description', 'ratings', 'date']
