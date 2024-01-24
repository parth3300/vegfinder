from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Restaurant, Review
from .serializers import RestaurantSerializer, CustomRestaurantSerializer, ReviewSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import RestaurantFilter



class RestaurantViewSet(ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RestaurantFilter

    def get_queryset(self):
        queryset = Restaurant.objects.all()
        state_id = self.request.query_params.get('state', None)

        if state_id:
            queryset = queryset.filter(state_id=state_id)

        return queryset


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
