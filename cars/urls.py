from django.urls import path
from cars.views import (
    car_list_today,
    car_list_yesterday,
    login_view,
    logout_view,
)

urlpatterns = [
    path('', car_list_today, name='car_list_today'),
    path('yesterday/', car_list_yesterday, name='car_list_yesterday'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
