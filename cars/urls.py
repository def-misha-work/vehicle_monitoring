from django.urls import path
from cars.views import (
    car_list,
    login_view,
    logout_view,
    set_time_period,
    set_plan_period,
)

urlpatterns = [
    path("", car_list, name="car_list"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("set_time_period/", set_time_period, name="set_time_period"),
    path("set_plan_period/", set_plan_period, name="set_plan_period"),
]
