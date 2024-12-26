import requests
import logging

from django.shortcuts import render, redirect
from django.contrib.auth import (
    login as auth_login,
    logout as auth_logout,
)
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from cars.models import Car, Jsession, User
from cars.constants import (
    URL_GET_JSESSION
)

logging.basicConfig(level=logging.INFO)


@login_required
def car_list(request):
    cars = Car.objects.all()
    paginator = Paginator(cars, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    user = request.user
    return render(
        request,
        "cars/index.html",
        {
            "page_obj": page_obj,
            'user': user
        }
    )


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # проверяем есть ли юзер в базе клиента
        url_get_jsession = (
            f"{URL_GET_JSESSION}?account={username}&password={password}"
        )
        response = requests.get(url_get_jsession)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logging.info(f"Ошибка запроса к api {e}")
            return render(
                request, "cars/login.html",
                {"error": "Неверный логин или пароль"}
            )

        data = response.json()
        if "jsession" not in data:
            logging.info("Ключ 'jsession' отсутствует в ответе")
            return render(
                request, "cars/login.html",
                {"error": "Неверный логин или пароль"}
            )
        # Создаем или получаем пользователя
        user, _ = User.objects.get_or_create(username=username)
        # Создаем или обновляем Jsession, связывая его с пользователем
        jsession, created = Jsession.objects.update_or_create(
            jsession=data["jsession"],
            # Обновляем поле user, если объект уже существует
            defaults={'user': user}
        )
        auth_login(request, user)
        return redirect('car_list')

    return render(request, "cars/login.html")


def logout_view(request):
    auth_logout(request)
    return redirect('login')
