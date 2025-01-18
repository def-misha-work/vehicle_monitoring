import random

from django.utils import timezone
from django.core.management.base import BaseCommand

from cars.models import Cars, Toplivo, DatchikVesa, Probeg, Vremya, Shini


class Command(BaseCommand):
    help = 'Создает случайные данные для существующих машин в таблицах Toplivo, DatchikVesa, Probeg, Vremya, Shini'

    def handle(self, *args, **kwargs):
        # Получаем все существующие машины
        cars = Cars.objects.all()

        for car in cars:
            # Создаем случайные данные для каждой таблицы
            toplivo = Toplivo.objects.create(
                dt=timezone.now(),
                ostatok_na_tekushchii_moment=random.uniform(1, 100),
                raskhod_za_period=random.uniform(1, 100),
                raskhod_za_poezdku=random.uniform(1, 100),
                raskhod_na_khkh_za_period=random.uniform(1, 100),
                raskhod_pod_nagruzkoi_za_period=random.uniform(1, 100),
                raskhod_v_puti_za_period=random.uniform(1, 100),
                raskhod_privedennii_g_t_km_za_period=random.uniform(1, 100),
                raskhod_privedennii_g_t_km_obshchii=random.uniform(1, 100),
            )

            datchik_vesa = DatchikVesa.objects.create(
                dt=timezone.now(),
                tekushchaya_nagruzka=random.uniform(1, 100),
                summarnii_ves_za_period=random.uniform(1, 100),
                min_ves_za_period=random.uniform(1, 100),
                max_ves_za_period=random.uniform(1, 100),
                srednii_ves_reisa_za_period=random.uniform(1, 100),
            )

            probeg = Probeg.objects.create(
                dt=timezone.now(),
                probeg_na_segodnya=random.uniform(1, 100),
                probeg_za_period=random.uniform(1, 100),
                kolichestvo_reisov=random.uniform(1, 100),
                kolichestvo_poezdok_za_period=random.uniform(1, 100),
            )

            vremya = Vremya.objects.create(
                dt=timezone.now(),
                vremya_s_nachala_perioda=random.uniform(1, 100),
                vremya_raboty_dvigatelya_za_period=random.uniform(1, 100),
                vremya_hkh_za_period=random.uniform(1, 100),
                motochasy_obshchie=random.uniform(1, 100),
                motochasy_za_period=random.uniform(1, 100),
            )

            shini = Shini.objects.create(
                dt=timezone.now(),
                davlenie_d_shinah=random.uniform(1, 100),
            )

            # Связываем созданные данные с машиной
            car.toplivo = toplivo
            car.datchik_vesa = datchik_vesa
            car.probeg = probeg
            car.vremya = vremya
            car.shini = shini
            car.save()

        self.stdout.write(
            self.style.SUCCESS('Случайные данные успешно добавлены для всех машин!')
        )
