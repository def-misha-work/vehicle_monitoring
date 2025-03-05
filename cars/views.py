import logging
from datetime import datetime, time, timedelta, timezone

import requests
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
# from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator
from django.db.models import (Avg, ExpressionWrapper, F, FloatField, Max, Min,
                              OuterRef, Q, Subquery, Sum)
from django.shortcuts import redirect, render
from django.utils import timezone as django_timezone

from cars.constants import URL_GET_JSESSION
from cars.forms import (PlanPeriodForm, SmenaOneForm, SmenaThreeForm,
                        SmenaTwoForm)
from cars.models import (DailyData, Jsession, PlanPeriod, SmenaOne, SmenaThree,
                         SmenaTwo, User, UserPassword)
from cars.utils import encrypt_password

logging.basicConfig(level=logging.INFO)


@login_required
def settings(request):
    user = request.user
    logging.info(f"User: {user}")

    if not Jsession.objects.filter(user=user).exists():
        messages.error(request, "Ошибка авторизации")
        return redirect("login")

    plan, created = PlanPeriod.objects.get_or_create(account_name=user)
    form_plan = PlanPeriodForm(
        initial={
            "plan_reisov": plan.plan_reisov,
            "plan_ves_za_period": plan.plan_ves_za_period,
        }
    )
    # передаем в форму текущие значения
    smena_one, created = SmenaOne.objects.get_or_create(account_name=user)
    smena_one = SmenaOneForm(initial={"start": smena_one.start, "end": smena_one.end})
    smena_two, created = SmenaTwo.objects.get_or_create(account_name=user)
    smena_two = SmenaTwoForm(initial={"start": smena_two.start, "end": smena_two.end})
    smena_three, created = SmenaThree.objects.get_or_create(account_name=user)
    smena_three = SmenaThreeForm(
        initial={"start": smena_three.start, "end": smena_three.end}
    )

    if request.method == "POST":
        if "submit_plan_period" in request.POST:
            form_plan = PlanPeriodForm(request.POST)
            if form_plan.is_valid():
                plan_period, created = PlanPeriod.objects.get_or_create(
                    account_name=user,
                    defaults={
                        "plan_reisov": form_plan.cleaned_data["plan_reisov"],
                        "plan_ves_za_period": form_plan.cleaned_data[
                            "plan_ves_za_period"
                        ],
                    },
                )
                if not created:
                    plan_period.plan_reisov = form_plan.cleaned_data["plan_reisov"]
                    plan_period.plan_ves_za_period = form_plan.cleaned_data[
                        "plan_ves_za_period"
                    ]
                    plan_period.save()
                return redirect("settings")

        if "submit_smena_one" in request.POST:
            form_time = SmenaOneForm(request.POST)
            if form_time.is_valid():
                smena_one, created = SmenaOne.objects.get_or_create(
                    account_name=user,
                    defaults={
                        "start": f"{form_time.cleaned_data['start']}:00",
                        "end": f"{form_time.cleaned_data['end']}:00",
                    },
                )
                if not created:
                    smena_one.start = form_time.cleaned_data["start"]
                    smena_one.end = form_time.cleaned_data["end"]
                    smena_one.save()
                return redirect("settings")

        if "submit_smena_two" in request.POST:
            form_time = SmenaTwoForm(request.POST)
            if form_time.is_valid():
                smena_two, created = SmenaTwo.objects.get_or_create(
                    account_name=user,
                    defaults={
                        "start": f"{form_time.cleaned_data['start']}:00",
                        "end": f"{form_time.cleaned_data['end']}:00",
                    },
                )
                if not created:
                    smena_two.start = form_time.cleaned_data["start"]
                    smena_two.end = form_time.cleaned_data["end"]
                    smena_two.save()
                return redirect("settings")

        if "submit_smena_three" in request.POST:
            form_time = SmenaThreeForm(request.POST)
            if form_time.is_valid():
                smena_three, created = SmenaThree.objects.get_or_create(
                    account_name=user,
                    defaults={
                        "start": f"{form_time.cleaned_data['start']}:00",
                        "end": f"{form_time.cleaned_data['end']}:00",
                    },
                )
                if not created:
                    smena_three.start = form_time.cleaned_data["start"]
                    smena_three.end = form_time.cleaned_data["end"]
                    smena_three.save()
                return redirect("settings")

    return render(
        request,
        "cars/settings.html",
        {
            "form_plan": form_plan,
            "form_smena_one": smena_one,
            "form_smena_two": smena_two,
            "form_smena_three": smena_three,
        },
    )


@login_required
def car_list(request):
    user = request.user
    logging.info(f"User: {user}")
    if not Jsession.objects.filter(user=user).exists():
        messages.error(request, "Ошибка авторизации")
        return redirect("login")

    # По умолчанию фильтруем за сегодня
    period = request.GET.get("period", "today")
    today = datetime.utcnow()

    # Подзапрос для получения последнего значения ostatok_na_tekushchii_moment
    last_ostatok_subquery = (
        DailyData.objects.filter(car=OuterRef("car"), dt__date=OuterRef("dt__date"))
        .order_by("-dt")
        .values("ostatok_na_tekushchii_moment")[:1]
    )

    # получаем данные для планы
    plan = PlanPeriod.objects.filter(account_name=user).order_by("-id").first()
    if not plan:
        # Если план не существует, создаем его с plan_reisov = 0
        plan = PlanPeriod.objects.create(
            account_name=user,
            plan_reisov=1,
            plan_ves_za_period=1,
        )
    # if period == "smena_sum":
    #     smena_one, created = SmenaOne.objects.get_or_create(account_name=user)
    #     smena_two, created = SmenaTwo.objects.get_or_create(account_name=user)
    #     smena_three, created = SmenaThree.objects.get_or_create(account_name=user)

    #     smena_one_start = datetime.combine(today, datetime.min.time()) + timedelta(
    #         hours=smena_one.start
    #     )
    #     smena_one_end = (
    #         datetime.combine(today, datetime.min.time())
    #         + timedelta(hours=smena_one.end)
    #         - timedelta(seconds=1)
    #     )

    #     smena_two_start = datetime.combine(today, datetime.min.time()) + timedelta(
    #         hours=smena_two.start
    #     )
    #     smena_two_end = (
    #         datetime.combine(today, datetime.min.time())
    #         + timedelta(hours=smena_two.end)
    #         - timedelta(seconds=1)
    #     )

    #     smena_three_start = datetime.combine(today, datetime.min.time()) + timedelta(
    #         hours=smena_three.start
    #     )
    #     smena_three_end = (
    #         datetime.combine(today, datetime.min.time())
    #         + timedelta(hours=smena_three.end)
    #         - timedelta(seconds=1)
    #     )

    #     combined_filter = (
    #         Q(dt__range=[smena_one_start, smena_one_end])
    #         | Q(dt__range=[smena_two_start, smena_two_end])
    #         | Q(dt__range=[smena_three_start, smena_three_end])
    #     )

    #     daily_data = (
    #         DailyData.objects.filter(combined_filter)
    #         .values("car__id_car")
    #         .annotate(
    #             raskhod_za_period=Sum("raskhod_za_period"),
    #             probeg_za_period=Sum("probeg_za_period"),
    #             tekushchaya_nagruzka=Sum("tekushchaya_nagruzka"),
    #             kolichestvo_reisov=Sum("kolichestvo_reisov"),
    #             summarnii_ves_za_period=Sum("summarnii_ves_za_period"),
    #             raskhod_privedennii_g_t_km_za_period=Sum(
    #                 "raskhod_privedennii_g_t_km_za_period"
    #             ),
    #             ostatok_na_tekushchii_moment=Subquery(last_ostatok_subquery),
    #             sum_kolichestvo_poezdok_za_period=Sum("kolichestvo_poezdok_za_period"),
    #             raskhod_za_poezdku=Sum("raskhod_za_poezdku"),
    #             raskhod_na_khkh_za_period=Sum("raskhod_na_khkh_za_period"),
    #             raskhod_pod_nagruzkoi_za_period=Sum("raskhod_pod_nagruzkoi_za_period"),
    #             avg_kolichestvo_poezdok_za_period=Avg("kolichestvo_poezdok_za_period"),
    #             min_ves_za_period=Min("min_ves_za_period"),
    #             max_ves_za_period=Min("max_ves_za_period"),
    #             avg_srednii_ves_reisa_za_period=Avg("srednii_ves_reisa_za_period"),
    #             chart_data_kolichestvo_reisov=ExpressionWrapper(
    #                 (F("kolichestvo_reisov") / plan.plan_reisov) * 100.0,
    #                 output_field=FloatField(),
    #             ),
    #             chart_data_tekushchaya_nagruzka=ExpressionWrapper(
    #                 (F("tekushchaya_nagruzka") / plan.plan_ves_za_period) * 100.0,
    #                 output_field=FloatField(),
    #             ),
    #         )
    #     )

    if period == "smena_one" or period == "smena_two" or period == "smena_three":
        if period == "smena_one":
            smena, created = SmenaOne.objects.get_or_create(account_name=user)
        if period == "smena_two":
            smena, created = SmenaTwo.objects.get_or_create(account_name=user)
        if period == "smena_three":
            smena, created = SmenaThree.objects.get_or_create(account_name=user)
        start_time = (
            datetime.combine(today, datetime.min.time())
            + timedelta(hours=smena.start)
        )
        if smena.start < smena.end:
            end_time = (
                start_time
                + timedelta(hours=(smena.end - smena.start))
                - timedelta(seconds=1)
            )
        else:
            end_time = (
                start_time
                + timedelta(hours=(24 - smena.start + smena.end))
                - timedelta(seconds=1)
            )
        start_time = start_time.replace(tzinfo=timezone.utc)
        end_time = end_time.replace(tzinfo=timezone.utc)
        print(f"start_time {start_time}, end_time {end_time}")
        daily_data = (
            DailyData.objects.filter(dt__range=[start_time, end_time])
            .values("car__id_car")
            .annotate(
                raskhod_za_period=Sum("raskhod_za_period"),
                probeg_za_period=Sum("probeg_za_period"),
                tekushchaya_nagruzka=Sum("tekushchaya_nagruzka"),
                kolichestvo_reisov=Sum("kolichestvo_reisov"),
                summarnii_ves_za_period=Sum("summarnii_ves_za_period"),
                raskhod_privedennii_g_t_km_za_period=Sum(
                    "raskhod_privedennii_g_t_km_za_period"
                ),
                ostatok_na_tekushchii_moment=Subquery(last_ostatok_subquery),
                sum_kolichestvo_poezdok_za_period=Sum("kolichestvo_poezdok_za_period"),
                raskhod_za_poezdku=Sum("raskhod_za_poezdku"),
                raskhod_na_khkh_za_period=Sum("raskhod_na_khkh_za_period"),
                raskhod_pod_nagruzkoi_za_period=Sum("raskhod_pod_nagruzkoi_za_period"),
                avg_kolichestvo_poezdok_za_period=Avg("kolichestvo_poezdok_za_period"),
                min_ves_za_period=Min("min_ves_za_period"),
                max_ves_za_period=Min("max_ves_za_period"),
                avg_srednii_ves_reisa_za_period=Avg("srednii_ves_reisa_za_period"),
                chart_data_kolichestvo_reisov=ExpressionWrapper(
                    (F("kolichestvo_reisov") / plan.plan_reisov) * 100.0,
                    output_field=FloatField(),
                ),
                chart_data_tekushchaya_nagruzka=ExpressionWrapper(
                    (F("tekushchaya_nagruzka") / plan.plan_ves_za_period) * 100.0,
                    output_field=FloatField(),
                ),
            )
        )
        print("sql: ", str(daily_data.query))

    if period == "today" or "smena_sum":
        daily_data = (
            DailyData.objects.filter(dt__date=today)
            .values("car__id_car")
            .annotate(
                raskhod_za_period=Sum("raskhod_za_period"),
                probeg_za_period=Sum("probeg_za_period"),
                tekushchaya_nagruzka=Sum("tekushchaya_nagruzka"),
                kolichestvo_reisov=Sum("kolichestvo_reisov"),
                summarnii_ves_za_period=Sum("summarnii_ves_za_period"),
                raskhod_privedennii_g_t_km_za_period=Sum(
                    "raskhod_privedennii_g_t_km_za_period"
                ),
                ostatok_na_tekushchii_moment=Subquery(last_ostatok_subquery),
                sum_kolichestvo_poezdok_za_period=Sum("kolichestvo_poezdok_za_period"),
                raskhod_za_poezdku=Sum("raskhod_za_poezdku"),
                raskhod_na_khkh_za_period=Sum("raskhod_na_khkh_za_period"),
                raskhod_pod_nagruzkoi_za_period=Sum("raskhod_pod_nagruzkoi_za_period"),
                avg_kolichestvo_poezdok_za_period=Avg("kolichestvo_poezdok_za_period"),
                min_ves_za_period=Min("min_ves_za_period"),
                max_ves_za_period=Min("max_ves_za_period"),
                avg_srednii_ves_reisa_za_period=Avg("srednii_ves_reisa_za_period"),
                chart_data_kolichestvo_reisov=ExpressionWrapper(
                    (F("kolichestvo_reisov") / plan.plan_reisov) * 100.0,
                    output_field=FloatField(),
                ),
                chart_data_tekushchaya_nagruzka=ExpressionWrapper(
                    (F("tekushchaya_nagruzka") / plan.plan_ves_za_period) * 100.0,
                    output_field=FloatField(),
                ),
            )
        )
        # print("sql: ", str(daily_data.query))

    if period == "yesterday":
        start_time = (
            datetime.combine(today, datetime.min.time())
            - timedelta(hours=24)
        )
        end_time = (
            datetime.combine(today, datetime.min.time())
            - timedelta(seconds=1)
            )
        daily_data = (
            DailyData.objects.filter(dt__date__range=[start_time, end_time])
            .values("car__id_car")
            .annotate(
                raskhod_za_period=Sum("raskhod_za_period"),
                probeg_za_period=Sum("probeg_za_period"),
                tekushchaya_nagruzka=Sum("tekushchaya_nagruzka"),
                kolichestvo_reisov=Sum("kolichestvo_reisov"),
                summarnii_ves_za_period=Sum("summarnii_ves_za_period"),
                raskhod_privedennii_g_t_km_za_period=Sum(
                    "raskhod_privedennii_g_t_km_za_period"
                ),
                # ostatok_na_tekushchii_moment=Subquery(last_ostatok_subquery),
                sum_kolichestvo_poezdok_za_period=Sum("kolichestvo_poezdok_za_period"),
                raskhod_za_poezdku=Sum("raskhod_za_poezdku"),
                raskhod_na_khkh_za_period=Sum("raskhod_na_khkh_za_period"),
                raskhod_pod_nagruzkoi_za_period=Sum("raskhod_pod_nagruzkoi_za_period"),
                avg_kolichestvo_poezdok_za_period=Avg("kolichestvo_poezdok_za_period"),
                min_ves_za_period=Min("min_ves_za_period"),
                max_ves_za_period=Min("max_ves_za_period"),
                avg_srednii_ves_reisa_za_period=Avg("srednii_ves_reisa_za_period"),
                chart_data_kolichestvo_reisov=ExpressionWrapper(
                    (F("kolichestvo_reisov") / plan.plan_reisov) * 100.0,
                    output_field=FloatField(),
                ),
                chart_data_tekushchaya_nagruzka=ExpressionWrapper(
                    (F("tekushchaya_nagruzka") / plan.plan_ves_za_period) * 100.0,
                    output_field=FloatField(),
                ),
            )
        )
        print(f"start_time {start_time} end_time {end_time}")

    if period == "7days":
        start_time = (
            datetime.combine(today, datetime.min.time())
            - timedelta(days=7)
        )
        end_time = (
            datetime.combine(today, datetime.min.time())
            - timedelta(seconds=1)
            )
        daily_data = (
            DailyData.objects.filter(
                dt__date__range=[start_time, end_time],
                # dt__hour__lt=12, dt__hour__gte=6,
            )
            .values("car__id_car")
            .annotate(
                raskhod_za_period=Sum("raskhod_za_period"),
                probeg_za_period=Sum("probeg_za_period"),
                tekushchaya_nagruzka=Sum("tekushchaya_nagruzka"),
                kolichestvo_reisov=Sum("kolichestvo_reisov"),
                summarnii_ves_za_period=Sum("summarnii_ves_za_period"),
                raskhod_privedennii_g_t_km_za_period=Sum(
                    "raskhod_privedennii_g_t_km_za_period"
                ),
                # ostatok_na_tekushchii_moment=Subquery(last_ostatok_subquery),
                sum_kolichestvo_poezdok_za_period=Sum("kolichestvo_poezdok_za_period"),
                raskhod_za_poezdku=Sum("raskhod_za_poezdku"),
                raskhod_na_khkh_za_period=Sum("raskhod_na_khkh_za_period"),
                raskhod_pod_nagruzkoi_za_period=Sum("raskhod_pod_nagruzkoi_za_period"),
                avg_kolichestvo_poezdok_za_period=Avg("kolichestvo_poezdok_za_period"),
                min_ves_za_period=Min("min_ves_za_period"),
                max_ves_za_period=Min("max_ves_za_period"),
                avg_srednii_ves_reisa_za_period=Avg("srednii_ves_reisa_za_period"),
            )
        )
        print(f"start_time {start_time} end_time {end_time}")

    # if period == "7days":
    #     start_date = today - timedelta(days=7)
    #     daily_data = (
    #         DailyData.objects.filter(dt__date__range=[start_date, today])
    #         .values("car__id_car")
    #         .annotate(
    #             raskhod_za_period=Sum("raskhod_za_period"),
    #             probeg_za_period=Sum("probeg_za_period"),
    #             tekushchaya_nagruzka=Sum("tekushchaya_nagruzka"),
    #             kolichestvo_reisov=Sum("kolichestvo_reisov"),
    #             summarnii_ves_za_period=Sum("summarnii_ves_za_period"),
    #             raskhod_privedennii_g_t_km_za_period=Sum(
    #                 "raskhod_privedennii_g_t_km_za_period"
    #             ),
    #             # ostatok_na_tekushchii_moment=Subquery(last_ostatok_subquery),
    #             sum_kolichestvo_poezdok_za_period=Sum("kolichestvo_poezdok_za_period"),
    #             raskhod_za_poezdku=Sum("raskhod_za_poezdku"),
    #             raskhod_na_khkh_za_period=Sum("raskhod_na_khkh_za_period"),
    #             raskhod_pod_nagruzkoi_za_period=Sum("raskhod_pod_nagruzkoi_za_period"),
    #             avg_kolichestvo_poezdok_za_period=Avg("kolichestvo_poezdok_za_period"),
    #             min_ves_za_period=Min("min_ves_za_period"),
    #             max_ves_za_period=Min("max_ves_za_period"),
    #             avg_srednii_ves_reisa_za_period=Avg("srednii_ves_reisa_za_period"),
    #         )
    #     )

    if period == "30days":
        start_time = (
            datetime.combine(today, datetime.min.time())
            - timedelta(days=30)
        )
        end_time = (
            datetime.combine(today, datetime.min.time())
            - timedelta(seconds=1)
            )
        daily_data = (
            DailyData.objects.filter(dt__date__range=[start_time, end_time])
            .values("car__id_car")
            .annotate(
                raskhod_za_period=Sum("raskhod_za_period"),
                probeg_za_period=Sum("probeg_za_period"),
                tekushchaya_nagruzka=Sum("tekushchaya_nagruzka"),
                kolichestvo_reisov=Sum("kolichestvo_reisov"),
                summarnii_ves_za_period=Sum("summarnii_ves_za_period"),
                raskhod_privedennii_g_t_km_za_period=Sum(
                    "raskhod_privedennii_g_t_km_za_period"
                ),
                # ostatok_na_tekushchii_moment=Subquery(last_ostatok_subquery),
                sum_kolichestvo_poezdok_za_period=Sum("kolichestvo_poezdok_za_period"),
                raskhod_za_poezdku=Sum("raskhod_za_poezdku"),
                raskhod_na_khkh_za_period=Sum("raskhod_na_khkh_za_period"),
                raskhod_pod_nagruzkoi_za_period=Sum("raskhod_pod_nagruzkoi_za_period"),
                avg_kolichestvo_poezdok_za_period=Avg("kolichestvo_poezdok_za_period"),
                min_ves_za_period=Min("min_ves_za_period"),
                max_ves_za_period=Min("max_ves_za_period"),
                avg_srednii_ves_reisa_za_period=Avg("srednii_ves_reisa_za_period"),
            )
        )
        print(f"start_time {start_time} end_time {end_time}")

    # Пагинация
    paginator = Paginator(daily_data, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Дата для диаграммы

    start_of_day = django_timezone.make_aware(datetime.combine(today, time.min))
    time_since_start_of_day = django_timezone.now() - start_of_day
    hours, remainder = divmod(time_since_start_of_day.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    # time_since_start = f"{hours:02}:{minutes:02}"

    # Передаем параметры GET-запроса в контекст
    get_params = request.GET.copy()
    if "page" in get_params:
        # Удаляем параметр "page", чтобы он не дублировался
        del get_params["page"]

    return render(
        request,
        "cars/index.html",
        {
            "page_obj": page_obj,
            "user": user,
            "period": period,
            # "time_since_start": time_since_start,
            "get_params": get_params.urlencode(),
            "plan": plan,
        },
    )


def login_view(request):
    if request.method != "POST":
        return render(request, "cars/login.html")
    username = request.POST["username"]
    password = request.POST["password"]
    # проверяем есть ли юзер в базе клиента
    url_get_jsession = f"{URL_GET_JSESSION}?account={username}&password={password}"
    response = requests.get(url_get_jsession)
    if response.status_code != 200:
        logging.warning("Ответ не 200")
        return render(request, "cars/login.html", {"error": "Ошибка авторизации"})
    if "message" in response.text:
        logging.warning(f"Ошибка api {response.text}")
        return render(request, "cars/login.html", {"error": "Ошибка авторизации"})
    data = response.json()
    if "jsession" not in data:
        logging.info("Ключ 'jsession' отсутствует в ответе")
        return render(
            request, "cars/login.html", {"error": "Неверный логин или пароль"}
        )

    # Создаем или получаем пользователя
    user, _ = User.objects.get_or_create(username=username)
    # Шифруем пароль, сохраняем его.
    encrypted_password = encrypt_password(password)
    UserPassword.objects.update_or_create(
        user=user, defaults={"encrypted_password": encrypted_password}
    )
    # Создаем или обновляем Jsession, связывая его с пользователем
    Jsession.objects.update_or_create(
        user=user, defaults={"jsession": data["jsession"]}
    )
    auth_login(request, user)
    return redirect("car_list")


def logout_view(request):
    auth_logout(request)
    return redirect("login")
