from django.urls import path, include
from django.urls import include, path
from rest_framework_nested import routers
from vegfinder import views

router = routers.DefaultRouter()
router.register('dharmshala', views.DharmshalaViewSet, basename='dharmshala')
router.register('restaurants', views.RestaurantViewSet, basename='restaurant')
router.register('hotels', views.HotelViewSet, basename='hotel')
router.register('cities', views.CityViewSet, basename='city')
router.register('states', views.StateViewSet, basename='state')
router.register('countries', views.CountryViewSet, basename='country')

dharmashala_router = routers.NestedDefaultRouter(
    router, 'dharmshala', lookup='dharmshala')
dharmashala_router.register(
    'reviews', views.ReviewViewSet, basename='dharmshala-review')

restaurant_router = routers.NestedDefaultRouter(
    router, 'restaurants', lookup='restaurant')
restaurant_router.register(
    'reviews', views.ReviewViewSet, basename='restaurant-review')

hotel_router = routers.NestedDefaultRouter(router, 'hotels', lookup='hotel')
hotel_router.register('reviews', views.ReviewViewSet, basename='hotel-review')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(dharmashala_router.urls)),
    path('', include(restaurant_router.urls)),
    path('', include(hotel_router.urls)),
    path('user/register/', views.UserProfileRegisterUserView.as_view(),
         name='user-register'),
    path('owner/register/', views.OwnerProfileRegisterUserView.as_view(),
         name='owner-register'),
    path('userverify/<slug:auth_token>', views.userverify, name='user-verify'),
    path('ownerverify/<slug:auth_token>',
         views.ownerverify, name='owner-verify'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

]
