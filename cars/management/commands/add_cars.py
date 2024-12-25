import random
from django.core.management.base import BaseCommand
from cars.models import Car, User


class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными для машин'

    def handle(self, *args, **kwargs):
        user = User.objects.get(username="test")
        jsession = user.jsession_set.first()
        for _ in range(10):
            car_number = random.randint(100, 999)
            mileage = random.randint(50, 120)
            flight = random.randint(8, 14)
            fuel = random.randint(80, 150)
            weight = random.randint(300, 700)
            shift_day = random.randint(40, 80)

            Car.objects.create(
                jsession=jsession,
                car_number=car_number,
                mileage=mileage,
                fuel=fuel,
                flight=flight,
                weight=weight,
                shift_day=shift_day
            )

        self.stdout.write(
            self.style.SUCCESS('Тестовые данные успешно добавлены!')
        )
