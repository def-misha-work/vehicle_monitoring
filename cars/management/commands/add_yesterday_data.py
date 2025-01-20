import random
from django.utils import timezone
from django.core.management.base import BaseCommand
from cars.models import Cars, Toplivo, DatchikVesa, Probeg, Vremya, Shini
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Добавляет тестовые данные за вчерашний день для существующих машин пользователя'

    def handle(self, *args, **kwargs):
        # Получаем тестового пользователя
        user = User.objects.get(username='test')

        # Получаем все машины, связанные с тестовым пользователем
        cars = Cars.objects.filter(account_name=user)

        if not cars.exists():
            self.stdout.write(self.style.WARNING('Нет машин, связанных с тестовым пользователем.'))
            return

        # Определяем вчерашний день
        yesterday = timezone.now() - timezone.timedelta(days=1)
        start_of_day = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timezone.timedelta(days=1)

        # Добавляем данные за вчерашний день для каждой машины
        for car in cars:
            # Проверяем, есть ли уже данные за вчера
            if (
                Toplivo.objects.filter(cars=car, dt__range=(start_of_day, end_of_day)).exists() or
                DatchikVesa.objects.filter(cars=car, dt__range=(start_of_day, end_of_day)).exists() or
                Probeg.objects.filter(cars=car, dt__range=(start_of_day, end_of_day)).exists() or
                Vremya.objects.filter(cars=car, dt__range=(start_of_day, end_of_day)).exists() or
                Shini.objects.filter(cars=car, dt__range=(start_of_day, end_of_day)).exists()
            ):
                self.stdout.write(self.style.WARNING(f'Данные за вчера уже существуют для машины {car.id_car}.'))
                continue

            # Создаем данные для Toplivo
            toplivo = Toplivo.objects.create(
                dt=yesterday,
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
                dt=yesterday,
                tekushchaya_nagruzka=random.uniform(1, 100),
                summarnii_ves_za_period=random.uniform(1, 100),
                min_ves_za_period=random.uniform(1, 100),
                max_ves_za_period=random.uniform(1, 100),
                srednii_ves_reisa_za_period=random.uniform(1, 100),
            )
            car.datchik_vesa = datchik_vesa  # Связываем с машиной

            # Создаем данные для Probeg
            probeg = Probeg.objects.create(
                dt=yesterday,
                probeg_na_segodnya=random.uniform(1, 100),
                probeg_za_period=random.uniform(1, 100),
                kolichestvo_reisov=random.uniform(1, 100),
                kolichestvo_poezdok_za_period=random.uniform(1, 100),
            )
            car.probeg = probeg  # Связываем с машиной

            # Создаем данные для Vremya
            vremya = Vremya.objects.create(
                dt=yesterday,
                vremya_s_nachala_perioda=random.uniform(1, 100),
                vremya_raboty_dvigatelya_za_period=random.uniform(1, 100),
                vremya_hkh_za_period=random.uniform(1, 100),
                motochasy_obshchie=random.uniform(1, 100),
                motochasy_za_period=random.uniform(1, 100),
            )
            car.vremya = vremya  # Связываем с машиной

            # Создаем данные для Shini
            shini = Shini.objects.create(
                dt=yesterday,
                davlenie_v_shinah=random.uniform(1, 100),
            )
            car.shini = shini  # Связываем с машиной

            # Сохраняем изменения в машине
            car.save()

            self.stdout.write(self.style.SUCCESS(f'Данные за вчера добавлены для машины {car.id_car}.'))

        self.stdout.write(self.style.SUCCESS('Данные за вчера успешно добавлены для всех машин.'))
