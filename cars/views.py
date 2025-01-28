import requests
import logging

from datetime import datetime, time, timedelta
from collections import defaultdict

from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import (
    login as auth_login,
    logout as auth_logout,
)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator
from django.db.models import Sum, F, Subquery, OuterRef

from cars.models import (
    Jsession,
    User,
    UserPassword,
    DailyData,
)
from cars.utils import encrypt_password
from cars.constants import URL_GET_JSESSION


logging.basicConfig(level=logging.INFO)


@login_required
def car_list(request):
    user = request.user
    logging.info(f"User: {user}")
    if not Jsession.objects.get(user=user):
        messages.error(request, "Ошибка авторизации")
        return redirect('login')

    # По умолчанию фильтруем за сегодня
    period = request.GET.get('period', 'today')
    # Сегодняшняя дата
    today = timezone.now().date()

    # Подзапрос для получения последнего значения ostatok_na_tekushchii_moment
    last_ostatok_subquery = DailyData.objects.filter(
        car=OuterRef('car'),
        dt__date=OuterRef('dt__date')
    ).order_by('-dt').values('ostatok_na_tekushchii_moment')[:1]

    result = defaultdict(lambda: {
        'raskhod_za_period': 0,
        'probeg_za_period': 0,
        'tekushchaya_nagruzka': 0,
        'kolichestvo_reisov': 0,
        'summarnii_ves_za_period': 0,
        'raskhod_privedennii_g_t_km_za_period': 0,
        'ostatok_na_tekushchii_moment': None
    })

    if period == "today":
        daily_data = DailyData.objects.filter(dt__date=today).values('car').annotate(
            car_name=F('car__id_car'),
            raskhod_za_period=Sum('raskhod_za_period'),
            probeg_za_period=Sum('probeg_za_period'),
            tekushchaya_nagruzka=Sum("tekushchaya_nagruzka"),
            kolichestvo_reisov=Sum("kolichestvo_reisov"),
            summarnii_ves_za_period=Sum("summarnii_ves_za_period"),
            raskhod_privedennii_g_t_km_za_period=Sum(
                "raskhod_privedennii_g_t_km_za_period"
            ),
            ostatok_na_tekushchii_moment=Subquery(last_ostatok_subquery)
        )

    if period == 'yesterday':
        # Вчерашняя дата
        yesterday = today - timedelta(days=1)
        daily_data = DailyData.objects.filter(dt__date=yesterday).values('car').annotate(
            car_name=F('car__id_car'),
            raskhod_za_period=Sum('raskhod_za_period'),
            probeg_za_period=Sum('probeg_za_period'),
            tekushchaya_nagruzka=Sum("tekushchaya_nagruzka"),
            kolichestvo_reisov=Sum("kolichestvo_reisov"),
            summarnii_ves_za_period=Sum("summarnii_ves_za_period"),
            raskhod_privedennii_g_t_km_za_period=Sum(
                "raskhod_privedennii_g_t_km_za_period"
            ),
            ostatok_na_tekushchii_moment=Subquery(last_ostatok_subquery)
        )

    if period == '7days':
        date_7 = today - timedelta(days=6)
        daily_data = DailyData.objects.filter(dt__gte=date_7).values('car').annotate(
            car_name=F('car__id_car'),
            raskhod_za_period=Sum('raskhod_za_period'),
            probeg_za_period=Sum('probeg_za_period'),
            tekushchaya_nagruzka=Sum("tekushchaya_nagruzka"),
            kolichestvo_reisov=Sum("kolichestvo_reisov"),
            summarnii_ves_za_period=Sum("summarnii_ves_za_period"),
            raskhod_privedennii_g_t_km_za_period=Sum(
                "raskhod_privedennii_g_t_km_za_period"
            ),
            ostatok_na_tekushchii_moment=Subquery(last_ostatok_subquery)
        )
        for entry in daily_data:
            car_id = entry['car']
            result[car_id]['raskhod_za_period'] += entry['raskhod_za_period']
            result[car_id]['probeg_za_period'] += entry['probeg_za_period']
            result[car_id]['tekushchaya_nagruzka'] += entry['tekushchaya_nagruzka']
            result[car_id]['kolichestvo_reisov'] += entry['kolichestvo_reisov']
            result[car_id]['summarnii_ves_za_period'] += entry['summarnii_ves_za_period']
            result[car_id]['raskhod_privedennii_g_t_km_za_period'] += entry['raskhod_privedennii_g_t_km_za_period']
            # Обновляем значение ostatok_na_tekushchii_moment из последнего элемента
            result[car_id]['ostatok_na_tekushchii_moment'] = entry['ostatok_na_tekushchii_moment']

        # Преобразуем defaultdict в обычный словарь
        final_result = {car_id: {**values, 'car_name': entry['car_name']} for car_id, values in result.items() for entry in daily_data if entry['car'] == car_id}
        daily_data = [{**values, 'car': car_id} for car_id, values in final_result.items()]
        # print(daily_data)

    if period == '30days':
        start_date = today - timedelta(days=29)
        daily_data = DailyData.objects.filter(dt__date__range=[start_date, today]).values('car').annotate(
            car_name=F('car__id_car'),
            raskhod_za_period=Sum('raskhod_za_period'),
            probeg_za_period=Sum('probeg_za_period'),
            tekushchaya_nagruzka=Sum("tekushchaya_nagruzka"),
            kolichestvo_reisov=Sum("kolichestvo_reisov"),
            summarnii_ves_za_period=Sum("summarnii_ves_za_period"),
            raskhod_privedennii_g_t_km_za_period=Sum(
                "raskhod_privedennii_g_t_km_za_period"
            ),
            ostatok_na_tekushchii_moment=Subquery(last_ostatok_subquery)
        ).distinct()


    # Агрегируем данные (например, суммируем показатели)
    # daily_data = daily_data.values('car').annotate(
    #     car_name=F('car__id_car'),
    #     raskhod_za_period=Sum('raskhod_za_period'),
    #     probeg_za_period=Sum('probeg_za_period'),
    #     tekushchaya_nagruzka=Sum("tekushchaya_nagruzka"),
    #     kolichestvo_reisov=Sum("kolichestvo_reisov"),
    #     summarnii_ves_za_period=Sum("summarnii_ves_za_period"),
    #     raskhod_privedennii_g_t_km_za_period=Sum(
    #         "raskhod_privedennii_g_t_km_za_period"
    #     ),
    #     ostatok_na_tekushchii_moment=Subquery(last_ostatok_subquery)
    # )

    # logging.info(f"Cars today: {daily_data.count()}")

    # Пагинация
    paginator = Paginator(daily_data, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Дата для диаграммы
    start_of_day = timezone.make_aware(datetime.combine(today, time.min))
    time_since_start_of_day = timezone.now() - start_of_day
    hours, remainder = divmod(time_since_start_of_day.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    time_since_start = f"{hours:02}:{minutes:02}"

    # Передаем параметры GET-запроса в контекст
    get_params = request.GET.copy()
    if 'page' in get_params:
        # Удаляем параметр 'page', чтобы он не дублировался
        del get_params['page']

    return render(
        request,
        "cars/index.html",
        {
            "page_obj": page_obj,
            "user": user,
            "period": period,
            'time_since_start': time_since_start,
            'get_params': get_params.urlencode(),
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
    # Шифруем пароль, сохраняем его.
    encrypted_password = encrypt_password(password)
    UserPassword.objects.update_or_create(
        user=user,
        defaults={'encrypted_password': encrypted_password}
    )
    # Создаем или обновляем Jsession, связывая его с пользователем
    Jsession.objects.update_or_create(
        user=user,
        defaults={'jsession': data["jsession"]}
    )
    auth_login(request, user)
    return redirect('car_list')


def logout_view(request):
    auth_logout(request)
    return redirect('login')
