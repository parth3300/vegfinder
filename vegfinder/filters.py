# filters.py

import django_filters
from django import forms
from .models import Restaurant, State, City, Country


class RestaurantFilter(django_filters.FilterSet):
    state = django_filters.ModelChoiceFilter(
        queryset=State.objects.all(),
        field_name='state',
        to_field_name='id',
        label='State',
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_state'}),
        null_label='All States',
    )

    city = django_filters.ModelChoiceFilter(
        queryset=City.objects.all(),
        field_name='city',
        to_field_name='id',
        label='City',
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_city'}),
        null_label='All Cities',
        method='filter_city_for_state',  # Specify the method for dynamic filtering
    )

    country = django_filters.ModelChoiceFilter(
        queryset=Country.objects.all(),
        field_name='country',
        to_field_name='id',
        label='Country',
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_country'}),
        null_label='All Countries',
    )

    def filter_city_for_state(self, queryset, name, value):
        if value:
            return queryset.filter(state_id=value)
        return queryset.none()  # Return an empty queryset if no state is selected

    class Meta:
        model = Restaurant
        fields = ['state', 'city', 'country']
