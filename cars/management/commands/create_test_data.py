import random
from django.utils import timezone
from django.core.management.base import BaseCommand
from cars.models import Cars, Toplivo, DatchikVesa, Probeg, Vremya, Shini
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Создает или обновляет данные для 15 машин и связанных таблиц за последние 90 дней'

    def handle(self, *args, **kwargs):
        # Создаем или получаем тестового пользователя
        user, created = User.objects.get_or_create(username='test')
        if created:
            user.set_password('test')
            user.save()

        # Создаем или обновляем 15 машин с id_car от 00001 до 00015
        for i in range(1, 16):
            id_car = f"{i:05d}"  # Форматируем id_car с ведущими нулями

            # Получаем или создаем машину
            car, car_created = Cars.objects.get_or_create(id_car=id_car)
            car.account_name.add(user)  # Связываем машину с тестовым пользователем

            # Создаем или обновляем данные за последние 90 дней
            for day in range(90):
                dt = timezone.now() - timezone.timedelta(days=day)

                # Создаем данные для Toplivo
                toplivo = Toplivo.objects.create(
                    dt=dt,
                    ostatok_na_tekushchii_moment=random.uniform(1, 100),
                    raskhod_za_period=random.uniform(1, 100),
                    raskhod_za_poezdku=random.uniform(1, 100),
                    raskhod_na_khkh_za_period=random.uniform(1, 100),
                    raskhod_pod_nagruzkoi_za_period=random.uniform(1, 100),
                    raskhod_v_puti_za_period=random.uniform(1, 100),
                    raskhod_privedennii_g_t_km_za_period=random.uniform(1, 100),
                    raskhod_privedennii_g_t_km_obshchii=random.uniform(1, 100),
                )
                car.toplivo = toplivo  # Связываем с машиной

                # Создаем данные для DatchikVesa
                datchik_vesa = DatchikVesa.objects.create(
                    dt=dt,
                    tekushchaya_nagruzka=random.uniform(1, 100),
                    summarnii_ves_za_period=random.uniform(1, 100),
                    min_ves_za_period=random.uniform(1, 100),
                    max_ves_za_period=random.uniform(1, 100),
                    srednii_ves_reisa_za_period=random.uniform(1, 100),
                )
                car.datchik_vesa = datchik_vesa  # Связываем с машиной

                # Создаем данные для Probeg
                probeg = Probeg.objects.create(
                    dt=dt,
                    probeg_na_segodnya=random.uniform(1, 100),
                    probeg_za_period=random.uniform(1, 100),
                    kolichestvo_reisov=random.uniform(1, 100),
                    kolichestvo_poezdok_za_period=random.uniform(1, 100),
                )
                car.probeg = probeg  # Связываем с машиной

                # Создаем данные для Vremya
                vremya = Vremya.objects.create(
                    dt=dt,
                    vremya_s_nachala_perioda=random.uniform(1, 100),
                    vremya_raboty_dvigatelya_za_period=random.uniform(1, 100),
                    vremya_hkh_za_period=random.uniform(1, 100),
                    motochasy_obshchie=random.uniform(1, 100),
                    motochasy_za_period=random.uniform(1, 100),
                )
                car.vremya = vremya  # Связываем с машиной

                # Создаем данные для Shini
                shini = Shini.objects.create(
                    dt=dt,
                    davlenie_v_shinah=random.uniform(1, 100),
                )
                car.shini = shini  # Связываем с машиной

                # Сохраняем изменения в машине
                car.save()

        self.stdout.write(
            self.style.SUCCESS('Данные успешно созданы или обновлены для 15 машин за последние 90 дней!')
        )
