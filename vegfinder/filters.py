import django_filters
from django import forms
from .models import Dharmshala, Restaurant, Hotel, City, State, Country


class DharmshalaFilter(django_filters.FilterSet):

    state = django_filters.ModelChoiceFilter(
        queryset=State.objects.all(),
        widget=forms.Select(attrs={'onchange': 'this.form.submit();'})
    )
    city = django_filters.ModelChoiceFilter(
        queryset=City.objects.none(),
        widget=forms.Select(),
        to_field_name='id',
    )

    class Meta:
        model = Dharmshala
        fields = ['state', 'city']

    def __init__(self, *args, **kwargs):
        super(DharmshalaFilter, self).__init__(*args, **kwargs)

        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                cities = City.objects.filter(state_id=state_id)
                self.filters['city'].field.queryset = cities
            except (ValueError, TypeError):
                pass


class RestaurantFilter(django_filters.FilterSet):
    country = django_filters.ModelChoiceFilter(
        queryset=Country.objects.all(),
        widget=forms.Select(attrs={'onchange': 'this.form.submit();'})
    )
    state = django_filters.ModelChoiceFilter(
        queryset=State.objects.none(),
        widget=forms.Select(attrs={'onchange': 'this.form.submit();'})
    )
    city = django_filters.ModelChoiceFilter(
        queryset=City.objects.none(),
        widget=forms.Select(),
        to_field_name='id',
    )

    class Meta:
        model = Restaurant
        fields = ['country', 'state', 'city']

    def __init__(self, *args, **kwargs):
        super(RestaurantFilter, self).__init__(*args, **kwargs)

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                states = State.objects.filter(country_id=country_id)
                self.filters['state'].field.queryset = states
            except (ValueError, TypeError):
                pass

        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                cities = City.objects.filter(state_id=state_id)
                self.filters['city'].field.queryset = cities
            except (ValueError, TypeError):
                pass


class HotelFilter(django_filters.FilterSet):
    country = django_filters.ModelChoiceFilter(
        queryset=Country.objects.all(),
        widget=forms.Select(attrs={'onchange': 'this.form.submit();'})
    )
    state = django_filters.ModelChoiceFilter(
        queryset=State.objects.none(),
        widget=forms.Select(attrs={'onchange': 'this.form.submit();'})
    )
    city = django_filters.ModelChoiceFilter(
        queryset=City.objects.none(),
        widget=forms.Select(),
        to_field_name='id',
    )

    class Meta:
        model = Hotel
        fields = ['country', 'state', 'city']

    def __init__(self, *args, **kwargs):
        super(HotelFilter, self).__init__(*args, **kwargs)

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                states = State.objects.filter(country_id=country_id)
                self.filters['state'].field.queryset = states
            except (ValueError, TypeError):
                pass

        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                cities = City.objects.filter(state_id=state_id)
                self.filters['city'].field.queryset = cities
            except (ValueError, TypeError):
                pass
