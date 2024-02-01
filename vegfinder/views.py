from rest_framework.permissions import BasePermission, IsAuthenticated
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Country, State, City, Owner, UserProfile, OwnerProfile, Dharmshala, Restaurant, Hotel, Review
from .serializers import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import DharmshalaFilter, RestaurantFilter, HotelFilter
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404, redirect
from rest_framework.response import Response
from rest_framework import status, generics
from .permissions import IsAdminOrReadOnly
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token
from django.contrib import messages
from django.contrib.auth.models import User
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout


class DefaultPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class CountryViewSet(ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticatedOrReadOnly]


class StateViewSet(ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        country_id = request.GET.get('country')
        if country_id:
            queryset = State.objects.filter(country_id=country_id)
        else:
            queryset = State.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CityViewSet(ModelViewSet):
    serializer_class = CitySerializer
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        state_id = self.request.query_params.get('state', None)
        if state_id:
            return City.objects.filter(state__id=state_id)
        return City.objects.all()


class OwnerViewSet(ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class DharmshalaViewSet(ModelViewSet):
    queryset = Dharmshala.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = DharmshalaFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            if Owner.objects.filter(id=self.request.user.id).exists():
                return CreateOwnerDharmshalaSerializer
            return CreateUserDharmshalaSerializer
        return DharmshalaSerializer

    def perform_create(self, serializer):
        if 'owner' in serializer.validated_data:
            user_name_id = self.request.user.id
            serializer.save(user_name_id=user_name_id)
        else:
            owner_id = self.request.user.id
            serializer.save(owner_id=owner_id, user_name_id=None)


class RestaurantViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = RestaurantFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            if Owner.objects.filter(id=self.request.user.id).exists():
                return CreateOwnerRestaurantSerializer
            return CreateUserRestaurantSerializer
        return RestaurantSerializer

    def perform_create(self, serializer):
        if 'owner' in serializer.validated_data:
            user_name_id = self.request.user.id
            serializer.save(user_name_id=user_name_id)
        else:
            owner_id = self.request.user.id
            serializer.save(owner_id=owner_id, user_name_id=None)


class HotelViewSet(ModelViewSet):
    queryset = Hotel.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = HotelFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            if Owner.objects.filter(id=self.request.user.id).exists():
                return CreateOwnerHotelSerializer
            return CreateUserHotelSerializer
        return HotelSerializer

    def perform_create(self, serializer):
        if 'owner' in serializer.validated_data:
            user_name_id = self.request.user.id
            serializer.save(user_name_id=user_name_id)
        else:
            owner_id = self.request.user.id
            serializer.save(owner_id=owner_id, user_name_id=None)


class ReviewViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if 'dharmshala_pk' in self.kwargs:
            return Review.objects.filter(dharmshala_id=self.kwargs['dharmshala_pk'])
        elif 'restaurant_pk' in self.kwargs:
            return Review.objects.filter(restaurant_id=self.kwargs['restaurant_pk'])
        elif 'hotel_pk' in self.kwargs:
            return Review.objects.filter(hotel_id=self.kwargs['hotel_pk'])

    def get_serializer_class(self):
        if 'dharmshala_pk' in self.kwargs:
            return ReviewDharmshalaSerializer
        elif 'restaurant_pk' in self.kwargs:
            return ReviewRestaurantSerializer
        elif 'hotel_pk' in self.kwargs:
            return ReviewHotelSerializer

    def perform_create(self, serializer):
        user_id = self.request.user.id
        serializer.save(user_id=user_id)
        if 'dharmshala_pk' in self.kwargs:
            serializer.save(dharmshala_id=self.kwargs['dharmshala_pk'])
        elif 'restaurant_pk' in self.kwargs:
            serializer.save(restaurant_id=self.kwargs['restaurant_pk'])
        elif 'hotel_pk' in self.kwargs:
            serializer.save(hotel_id=self.kwargs['hotel_pk'])

    def perform_destroy(self, instance):
        user = self.request.user

        if user.is_staff or instance.user == user:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN, data={'detail': 'You do not have permission to delete this review.'})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user = self.request.user

        if user.is_staff or instance.user == user:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

        return Response(status=status.HTTP_403_FORBIDDEN, data={'detail': 'You do not have permission to view this review.'})


class UserProfileRegisterUserView(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileRegisterUserSerializer

    def create(self, request, *args, **kwargs):
        if request.method == 'POST':
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')

            try:
                if User.objects.filter(username=username).exists():
                    return Response({'error': 'Username is taken'}, status=status.HTTP_400_BAD_REQUEST)
                elif User.objects.filter(email=email).exists():
                    return Response({'error': 'Email is taken'}, status=status.HTTP_400_BAD_REQUEST)

                user_obj = User(username=username, email=email)
                user_obj.set_password(password)
                user_obj.save()

                auth_token = str(uuid.uuid4())
                userprofile_obj = UserProfile.objects.create(
                    user=user_obj, auth_token=auth_token)
                userprofile_obj.save()

                self.send_activation_mail(email, userprofile_obj.auth_token)

                return Response({'success': 'We have sent an email to activate your account Please check your mail'}, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({'error': f'An error {e} occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'error': 'Method Not Allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def send_activation_mail(self, email, auth_token):
        subject = 'Your account needs to be verified'
        message = f'Hi, paste the link to verify your account http://127.0.0.1:8000/vegfinder/userverify/{auth_token}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        send_mail(subject, message, email_from, recipient_list)


def userverify(request, auth_token):
    try:
        profile_obj = UserProfile.objects.filter(auth_token=auth_token).first()

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('http://127.0.0.1:8000/vegfinder/login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account is now verified.')
            return redirect('http://127.0.0.1:8000/vegfinder/login')
        else:
            return Response({'error': 'The link is invalid '}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': f'An error {e} occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OwnerProfileRegisterUserView(generics.CreateAPIView):
    queryset = OwnerProfile
    serializer_class = OwnerProfileRegisterUserSerializer

    def create(self, request, *args, **kwargs):
        if request.method == 'POST':
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')
            first_name = request.data.get('first_name')
            last_name = request.data.get('last_name')
            profile_pic = request.data.get('profile_pic')

            try:
                user_obj = User(username=username,
                                email=email, first_name=first_name, last_name=last_name)
                user_obj.set_password(password)
                user_obj.save()

                auth_token = uuid.uuid4()
                ownerprofile_obj = OwnerProfile.objects.create(user=user_obj,
                                                               profile_pic=profile_pic, auth_token=auth_token)
                self.send_activation_mail(email, ownerprofile_obj.auth_token)

                return Response({'success': 'We have sent an email to activate your account please check your email'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': f'an error {e} occured'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'error': 'method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def send_activation_mail(self, email, auth_token):
        subject = 'Your account needs to be verified'
        message = f'Hi, paste the link to verify your account http://127.0.0.1:8000/vegfinder/ownerverify/{auth_token}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email, ]
        send_mail(subject, message, email_from, recipient_list)


def ownerverify(request, auth_token):
    try:
        profile_obj = OwnerProfile.objects.filter(
            auth_token=auth_token).first()

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('http://127.0.0.1:8000/vegfinder/login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account is now verified.')
            return redirect('http://127.0.0.1:8000/vegfinder/login')
        else:
            return Response({'error': 'The link is invalid '}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': f'An error {e} occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user_obj = authenticate(username=username, password=password)

        if user_obj:
            profile_obj = None

            if UserProfile.objects.filter(user=user_obj).exists():
                profile_obj = UserProfile.objects.get(user=user_obj)
            elif OwnerProfile.objects.filter(user=user_obj).exists():
                profile_obj = OwnerProfile.objects.get(user=user_obj)

            try:
                if profile_obj and profile_obj.is_verified:
                    login(request, user_obj)
                    return Response({'success': 'Login successful'})
                elif profile_obj and not profile_obj.is_verified:
                    return Response({'error': 'Account not verified'}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    return Response({'error': 'Invalid profile'}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({'error': f'An error {e} occurred'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({'success': 'Logout successful'})
