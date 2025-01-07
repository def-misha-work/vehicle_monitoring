import requests
import logging

from django.shortcuts import render, redirect
from django.contrib.auth import (
    login as auth_login,
    logout as auth_logout,
)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator
from cars.models import Jsession, User
from cars.constants import (
    URL_GET_JSESSION
)
from cars.utils import (
    get_tech,
    get_fuel_and_mileage,
    get_weight,
)

logging.basicConfig(level=logging.INFO)


@cache_page(60 * 15)
@login_required
def car_list(request):
    user = request.user
    try:
        jsession_obj = Jsession.objects.get(user=user)
        jsession = jsession_obj.jsession
    except Jsession.DoesNotExist:
        messages.error(request, "Ошибка авторизации")
        return redirect('login')

    # Получаем технику
    devidno = get_tech(jsession)
    logging.info(f"Это devidno {devidno}")
    if devidno is False:
        logging.info("Не получили технику")
        messages.error(request, "Время сессии истекло")
        return redirect('login')

    # Получаю топливо и пробег
    result = get_fuel_and_mileage(jsession, devidno)
    if result is False:
        logging.info("Не получили топливо или пробег")
        messages.error(request, "Время сессии истекло")
        return redirect('login')

    fuel_yl, mileage_lc = result
    logging.info(f"Это fuel_yl {fuel_yl}")
    logging.info(f"Это mileage_lc {mileage_lc}")

    # Получаем вес
    weight_p2 = get_weight(jsession, devidno)
    # Создаем страницы
    combined_data = zip(devidno, mileage_lc, fuel_yl, weight_p2)
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
    if request.method != 'POST':
        return render(request, "cars/login.html")
    username = request.POST['username']
    password = request.POST['password']
    # проверяем есть ли юзер в базе клиента
    url_get_jsession = (
        f"{URL_GET_JSESSION}?account={username}&password={password}"
    )
    response = requests.get(url_get_jsession)
    if response.status_code != 200:
        logging.warning("Ответ не 200")
        return render(
            request, "cars/login.html",
            {"error": "Ошибка авторизации"}
        )
    if "message" in response.text:
        logging.warning(f"Ошибка api {response.text}")
        return render(
            request, "cars/login.html",
            {"error": "Ошибка авторизации"}
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
    Jsession.objects.update_or_create(
        user=user,  # Ищем запись по пользователю
        defaults={'jsession': data["jsession"]}  # Обновляем поле jsession
    )
    auth_login(request, user)
    return redirect('car_list')


def logout_view(request):
    auth_logout(request)
    return redirect('login')
