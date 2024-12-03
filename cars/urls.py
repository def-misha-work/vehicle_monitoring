from django.urls import path
from .views import car_list

urlpatterns = [
    path('', car_list, name='car_list'),
]
