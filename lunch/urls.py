from django.urls import path, include
from rest_framework import routers
from .views import RestaurantViewSet, MenuViewSet

router = routers.DefaultRouter()
router.register(r'restaurants', RestaurantViewSet, basename='restaurants')
router.register(r'menus', MenuViewSet, basename='menus')

urlpatterns = [
    path('', include(router.urls)),
]
