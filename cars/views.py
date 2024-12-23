import requests
import logging

from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    login as auth_login,
    logout as auth_logout
)
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from cars.models import Car
from cars.constants import (
    URL_LOGIN,
    USER_LOGIN,
    USER_PASSWORD,
)

logging.basicConfig(level=logging.INFO)


@login_required
def car_list(request):
    cars = Car.objects.all()
    paginator = Paginator(cars, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "cars/index.html", {"page_obj": page_obj})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # проверяем есть ли юзер в базе клиента
        URL_GET_ENTER = (
            f"{URL_LOGIN}?account={USER_LOGIN}&password={USER_PASSWORD}"
        )
        response = requests.get(URL_GET_ENTER)
        try:
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.HTTPError as e:
            logging.info(f"Ошибка запроса к api {e}")
            return render(
                request, "cars/login.html",
                {"error": "Неверный логин или пароль"}
            )
        # TODO тут надо сделать запрос к базе данных
        # на предмет наличия "jsession"
        if "jsession" not in data:
            logging.info("Ключ 'jsession' отсутствует в ответе")
            return render(
                request, "cars/login.html",
                {"error": "Неверный логин или пароль"}
            )
        if data["jsession"] == "817328fdd0274ce283ec715b215d5b4c":
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('car_list')
            else:
                return render(
                    request, "cars/login.html",
                    {"error": "Неверный логин или пароль"}
                )
        # TODO убрать после норм авторизации
        else:
            return render(
                request, "cars/login.html",
                {"error": "Неверный логин или пароль"}
            )
    return render(request, "cars/login.html")


def logout_view(request):
    auth_logout(request)
    return redirect('login')
