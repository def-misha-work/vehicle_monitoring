from django.urls import path
from cars.views import (
    car_list,
    login_view,
    logout_view,
)

urlpatterns = [
    path('', car_list, name='car_list'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
