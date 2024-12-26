import requests
import logging

from django.shortcuts import render, redirect
from django.contrib.auth import (
    login as auth_login,
    logout as auth_logout,
)
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from cars.models import Jsession, User
from cars.constants import (
    URL_GET_JSESSION
)
from cars.utils import (
    get_tech,
    get_fuel_and_mileage,
)

logging.basicConfig(level=logging.INFO)


@login_required
def car_list(request):
    user = request.user
    try:
        jsession_obj = Jsession.objects.get(user=user)
        jsession = jsession_obj.jsession
    except Jsession.DoesNotExist:
        return render(
                request, "cars/login.html",
                {"error": "Ошибка авторизации"}
            )

    # Получаем технику
    result = get_tech(jsession)
    if result is False:
        return render(
                request, "cars/login.html",
                {"error": "Ошибка авторизации"}
            )
        logging.critical("Не получили технику")
    else:
        vehicle_ids, devidno = result
    # logging.info(f"Это vehicle_ids {vehicle_ids}")
    # logging.info(f"Это devidno {devidno}")

    # Получаю топливо и пробег
    result = get_fuel_and_mileage(jsession, devidno)
    if result is False:
        return render(
                request, "cars/login.html",
                {"error": "Ошибка авторизации"}
            )
        logging.critical("Не получили топливо или пробег")
    fuel_yl, mileage_lc = result
    logging.info(f"Это fuel_yl {fuel_yl}")
    logging.info(f"Это mileage_lc {mileage_lc}")

    # Создаем страницы
    combined_data = zip(vehicle_ids, mileage_lc, fuel_yl)
    paginator = Paginator(list(combined_data), 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "cars/index.html",
        {
            "page_obj": page_obj,
            "user": user,
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
        try:
            response = requests.get(url_get_jsession)
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
