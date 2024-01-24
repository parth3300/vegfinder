from django.urls import include, path
from rest_framework_nested import routers
from vegfinder import views


router = routers.DefaultRouter()
router.register('restaurants', views.RestaurantViewSet)


restaurant_router = routers.NestedDefaultRouter(
    router, 'restaurants', lookup='restaurant')
restaurant_router.register('reviews', views.ReviewViewSet,
                           basename='restaurant-review')

urlpatterns = router.urls + restaurant_router.urls
