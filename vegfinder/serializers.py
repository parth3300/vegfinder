from rest_framework import serializers
from .models import Country, State, City, Owner, User, Dharmshala, Restaurant, Hotel, Review


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']


class StateSerializer(serializers.ModelSerializer):
    country = serializers.SerializerMethodField()

    def get_country(self, state):
        return state.country.name

    class Meta:
        model = State
        fields = ['id', 'name', 'country']


class CitySerializer(serializers.ModelSerializer):
    state = serializers.SerializerMethodField()

    def get_state(self, city):
        return city.state.name

    class Meta:
        model = City
        fields = ['id', 'name', 'state']


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ['id', 'name', 'dharmshala_owner',
                  'restaurants_owner', 'hotels_owner', 'contact']


class DharmshalaSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    def get_address(self, dharmshala):
        return f'{dharmshala.block_no} {dharmshala.street}, {dharmshala.city.name}, {dharmshala.state.name} - {dharmshala.pincode}'

    def get_owner(self, dharmshala):
        return dharmshala.owner.user.username

    def get_user_name(self, dharmshala):
        return dharmshala.user_name.username if dharmshala.user_name else None

    class Meta:
        model = Dharmshala
        fields = ['id', 'user_name', 'owner', 'title', 'images', 'address', 'rooms',
                  'facilties', 'rent', 'restriction', 'contact']


class CreateUserDharmshalaSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(read_only=True)
    owner_name = serializers.SerializerMethodField()

    def get_owner_name(self, restaurant):
        return restaurant.owner.user.username

    class Meta:
        model = Dharmshala
        fields = ['id', 'title', 'user_name', 'owner', 'owner_name', 'images', 'block_no', 'street', 'city', 'state',
                  'pincode', 'rooms', 'facilties', 'rent', 'restriction', 'contact']


class CreateOwnerDharmshalaSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(read_only=True)
    state = serializers.PrimaryKeyRelatedField(queryset=State.objects.all())
    city = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(), required=False)

    class Meta:
        model = Dharmshala
        fields = ['id', 'title',  'owner', 'images', 'block_no', 'street', 'city', 'state',
                  'pincode', 'rooms', 'facilties', 'rent', 'restriction', 'contact']

    def create(self, validated_data):
        # Extract the state ID from the validated data
        state_id = validated_data.pop('state')

        # Fetch the city based on the state
        city_queryset = City.objects.filter(state_id=state_id)
        if city_queryset.exists():
            validated_data['city'] = city_queryset.first()

        # Create and return the Dharmshala instance
        return Dharmshala.objects.create(**validated_data)


class RestaurantSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    def get_address(self, restaurant):
        return f'{restaurant.block_no} {restaurant.street}, {restaurant.city.name}, {restaurant.state.name} - {restaurant.pincode}'

    def get_owner(self, restaurant):
        return restaurant.owner.user.username

    def get_user_name(self, restaurant):
        return restaurant.user_name.username if restaurant.user_name else None

    class Meta:
        model = Restaurant
        fields = ['id', 'title', 'user_name', 'owner',
                  'images', 'address',  'contact', 'ratings']


class CreateUserRestaurantSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(read_only=True)
    owner_name = serializers.SerializerMethodField()

    def get_owner_name(self, restaurant):
        return restaurant.owner.user.username

    class Meta:
        model = Restaurant
        fields = ['id', 'title', 'user_name', 'owner', 'owner_name', 'images', 'block_no', 'street',
                  'city', 'state', 'country', 'pincode', 'contact', 'ratings']


class CreateOwnerRestaurantSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(read_only=True)

    class Meta:
        model = Restaurant
        fields = ['id', 'title',  'owner', 'images', 'block_no', 'street',
                  'city', 'state', 'country', 'pincode', 'contact', 'ratings']


class HotelSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()

    def get_address(self, hotel):
        return f'{hotel.block_no} {hotel.street}, {hotel.city.name}, {hotel.state.name} - {hotel.pincode}'

    def get_owner(self, hotel):
        return hotel.owner.user.username

    def get_user_name(self, hotel):
        return hotel.user_name.username if hotel.user_name else None

    class Meta:
        model = Hotel
        fields = ['id', 'title', 'user_name', 'owner',
                  'images', 'address', 'rent', 'contact', 'ratings']


class CreateUserHotelSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(read_only=True)
    owner_name = serializers.SerializerMethodField()

    def get_owner_name(self, restaurant):
        return restaurant.owner.user.username

    class Meta:
        model = Hotel
        fields = ['id', 'title', 'user_name', 'owner', 'owner_name', 'images', 'block_no', 'street',
                  'city', 'state', 'country', 'pincode', 'contact', 'rent', 'ratings']


class CreateOwnerHotelSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(read_only=True)

    class Meta:

        model = Hotel
        fields = ['id', 'title', 'owner', 'images', 'block_no', 'street',
                  'city', 'state', 'country', 'pincode', 'contact', 'rent', 'ratings']


class ReviewDharmshalaSerializer(serializers.ModelSerializer):
    dharmshala = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    def get_dharmshala(self, reviewdharmshala):
        return reviewdharmshala.dharmshala.title

    def get_name(self, reviewdharmshala):
        return reviewdharmshala.user.username

    class Meta:
        model = Review
        fields = ['id', 'name', 'dharmshala', 'description', 'ratings', 'date']


class ReviewRestaurantSerializer(serializers.ModelSerializer):
    restaurant = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    def get_restaurant(self, reviewrestaurant):
        return reviewrestaurant.restaurant.title

    def get_name(self, reviewrestaurant):
        return reviewrestaurant.user.username

    class Meta:
        model = Review
        fields = ['id', 'name', 'restaurant', 'description', 'ratings', 'date']


class ReviewHotelSerializer(serializers.ModelSerializer):
    hotel = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    def get_hotel(self, reviewhotel):
        return reviewhotel.hotel.title

    def get_name(self, reviewhotel):
        return reviewhotel.user.username

    class Meta:
        model = Review
        fields = ['id', 'name', 'hotel', 'description', 'ratings', 'date']


class UserProfileRegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']


class OwnerProfileRegisterUserSerializer(serializers.ModelSerializer):
    profile_pic = serializers.ImageField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password',
                  'first_name', 'last_name', 'profile_pic']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True)
