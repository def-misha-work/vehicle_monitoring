import random
from datetime import datetime, time, timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from cars.models import Cars, DailyData  # Импортируем новые модели


class Command(BaseCommand):
    help = "Создает или обновляет тестовые данные"

    def handle(self, *args, **kwargs):
        # Количество машин и дней для создания данных
        num_cars = 3  # Количество машин
        num_days = 30  # Количество дней

        # Создаем или получаем тестового пользователя
        user, user_created = User.objects.get_or_create(username="test")
        if user_created:
            self.stdout.write(self.style.SUCCESS('Пользователь "test" создан.'))

        # Времена, в которые будут создаваться данные
        times_of_day = [time(9, 0), time(14, 0), time(19, 0)]

        # Создаем тестовые данные для машин
        for i in range(1, num_cars + 1):
            id_car = f"{i:05d}"  # Форматируем id_car с ведущими нулями

            # Получаем или создаем машину
            car, car_created = Cars.objects.get_or_create(id_car=id_car)
            car.account_name.add(user)  # Связываем машину с пользователем

            # Создаем данные за последние `num_days` дней
            for day in range(num_days):
                # Получаем дату с 0:00
                current_date = datetime.now().date() - timedelta(days=day)

                # Создаем данные для каждого времени в течение дня
                for time_of_day in times_of_day:
                    target_datetime = datetime.combine(current_date, time_of_day)
                    self.stdout.write(
                        self.style.NOTICE(f"Target datetime: {target_datetime}.")
                    )

                    # Создаем или получаем объект DailyData
                    daily_data, created = DailyData.objects.get_or_create(
                        car=car,
                        dt=target_datetime,
                        defaults={
                            # Топливо
                            "ostatok_na_tekushchii_moment": random.uniform(1, 100),
                            "raskhod_za_period": random.uniform(1, 100),
                            "raskhod_za_poezdku": random.uniform(1, 100),
                            "raskhod_na_khkh_za_period": random.uniform(1, 100),
                            "raskhod_pod_nagruzkoi_za_period": random.uniform(1, 100),
                            "raskhod_v_puti_za_period": random.uniform(1, 100),
                            "raskhod_privedennii_g_t_km_za_period": random.uniform(
                                1, 100
                            ),
                            "raskhod_privedennii_g_t_km_obshchii": random.uniform(
                                1, 100
                            ),
                            # Датчик веса
                            "tekushchaya_nagruzka": random.uniform(1, 100),
                            "summarnii_ves_za_period": random.uniform(1, 100),
                            "min_ves_za_period": random.uniform(1, 100),
                            "max_ves_za_period": random.uniform(1, 100),
                            "srednii_ves_reisa_za_period": random.uniform(1, 100),
                            # Пробег
                            "probeg_na_segodnya": random.uniform(1, 100),
                            "probeg_za_period": random.uniform(1, 100),
                            "kolichestvo_reisov": random.uniform(1, 100),
                            "kolichestvo_poezdok_za_period": random.uniform(1, 100),
                            # Время
                            "vremya_s_nachala_perioda": random.uniform(1, 100),
                            "vremya_raboty_dvigatelya_za_period": random.uniform(
                                1, 100
                            ),
                            "vremya_hkh_za_period": random.uniform(1, 100),
                            "motochasy_obshchie": random.uniform(1, 100),
                            "motochasy_za_period": random.uniform(1, 100),
                            # Шины
                            "davlenie_v_shinah": random.uniform(1, 100),
                        },
                    )

                    if created:
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Данные для машины {car.id_car} на {target_datetime} созданы."
                            )
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(
                                f"Данные для машины {car.id_car} на {target_datetime} уже существуют."
                            )
                        )

        self.stdout.write(
            self.style.SUCCESS("Тестовые данные успешно созданы или обновлены.")
        )
