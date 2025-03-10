import logging

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class UserPassword(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="encrypted_password"
    )
    encrypted_password = models.CharField(max_length=255)


class Jsession(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="jsession")
    jsession = models.CharField(max_length=255)

    def __str__(self):
        return f"jsession: {self.jsession}"


class PlanPeriod(models.Model):
    account_name = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    plan_reisov = models.IntegerField(verbose_name="План по рейсам", default=1)
    plan_ves_za_period = models.IntegerField(
        verbose_name="План по тоннам (весу)", default=1
    )


class SmenaOne(models.Model):
    account_name = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    start = models.IntegerField(verbose_name="Начало смены (часы)", default=8)
    end = models.IntegerField(verbose_name="Окончание смены (часы)", default=16)

    def __str__(self):
        return f"Смена с {self.start}:00 по {self.end}:00"

    class Meta:
        verbose_name = "Смена"
        verbose_name_plural = "Смены"


class SmenaTwo(models.Model):
    account_name = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    start = models.IntegerField(verbose_name="Начало смены (часы)", default=16)
    end = models.IntegerField(verbose_name="Окончание смены (часы)", default=0)

    def __str__(self):
        return f"Смена с {self.start}:00 по {self.end}:00"

    class Meta:
        verbose_name = "Смена"
        verbose_name_plural = "Смены"


class SmenaThree(models.Model):
    account_name = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    start = models.IntegerField(verbose_name="Начало смены (часы)", default=0)
    end = models.IntegerField(verbose_name="Окончание смены (часы)", default=8)

    def __str__(self):
        return f"Смена с {self.start}:00 по {self.end}:00"

    class Meta:
        verbose_name = "Смена"
        verbose_name_plural = "Смены"


class SmenaAll(models.Model):
    account_name = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    start = models.IntegerField(verbose_name="Начало смены (часы)", default=0)
    end = models.IntegerField(verbose_name="Окончание смены (часы)", default=24)

    def __str__(self):
        return f"Смена с {self.start}:00 по {self.end}:00"


class Cars(models.Model):
    id_car = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Идентификатор машины",
    )
    account_name = models.ManyToManyField(
        User,
        related_name="cars",
        verbose_name="Пользователи",
        blank=True,
    )

    class Meta:
        verbose_name = "Машина"
        verbose_name_plural = "Машины"

    def __str__(self):
        return f"Машина: {self.id_car}"


class DailyData(models.Model):
    car = models.ForeignKey(
        Cars,
        related_name="daily_data",
        verbose_name="Машина",
        on_delete=models.CASCADE,
    )
    dt = models.DateTimeField(
        default=timezone.now,
        verbose_name="Дата и время",
    )

    # Топливо
    ostatok_na_tekushchii_moment = models.FloatField(
        verbose_name="Остаток на текущий момент",
        null=True,
        blank=True,
    )
    raskhod_za_period = models.FloatField(
        verbose_name="Расход за период",
        null=True,
        blank=True,
    )
    raskhod_za_poezdku = models.FloatField(
        verbose_name="Расход за поездку",
        null=True,
        blank=True,
    )
    raskhod_na_khkh_za_period = models.FloatField(
        verbose_name="Расход на ХХ за период",
        null=True,
        blank=True,
    )
    raskhod_pod_nagruzkoi_za_period = models.FloatField(
        verbose_name="Расход под нагрузкой за период",
        null=True,
        blank=True,
    )
    raskhod_v_puti_za_period = models.FloatField(
        verbose_name="Расход в пути за период",
        null=True,
        blank=True,
    )
    raskhod_privedennii_g_t_km_za_period = models.FloatField(
        verbose_name="Приведенный расход г/т*км за период",
        null=True,
        blank=True,
    )
    raskhod_privedennii_g_t_km_obshchii = models.FloatField(
        verbose_name="Общий приведенный расход г/т*км",
        null=True,
        blank=True,
    )

    # Датчик веса
    tekushchaya_nagruzka = models.FloatField(
        verbose_name="Текущая нагрузка",
        null=True,
        blank=True,
    )
    summarnii_ves_za_period = models.FloatField(
        verbose_name="Суммарный вес за период",
        null=True,
        blank=True,
    )
    min_ves_za_period = models.FloatField(
        verbose_name="Минимальный вес за период",
        null=True,
        blank=True,
    )
    max_ves_za_period = models.FloatField(
        verbose_name="Максимальный вес за период",
        null=True,
        blank=True,
    )
    srednii_ves_reisa_za_period = models.FloatField(
        verbose_name="Средний вес рейса за период",
        null=True,
        blank=True,
    )

    # Пробег
    probeg_na_segodnya = models.FloatField(
        verbose_name="Пробег на сегодня",
        null=True,
        blank=True,
    )
    probeg_za_period = models.FloatField(
        verbose_name="Пробег за период",
        null=True,
        blank=True,
    )
    kolichestvo_reisov = models.FloatField(
        verbose_name="Количество рейсов",
        null=True,
        blank=True,
    )
    kolichestvo_poezdok_za_period = models.FloatField(
        verbose_name="Количество поездок за период",
        null=True,
        blank=True,
    )

    # Время
    vremya_s_nachala_perioda = models.FloatField(
        verbose_name="Время с начала периода",
        null=True,
        blank=True,
    )
    vremya_raboty_dvigatelya_za_period = models.FloatField(
        verbose_name="Время работы двигателя за период",
        null=True,
        blank=True,
    )
    vremya_hkh_za_period = models.FloatField(
        verbose_name="Время ХХ за период",
        null=True,
        blank=True,
    )
    motochasy_obshchie = models.FloatField(
        verbose_name="Моточасы общие",
        null=True,
        blank=True,
    )
    motochasy_za_period = models.FloatField(
        verbose_name="Моточасы за период",
        null=True,
        blank=True,
    )

    # Шины
    davlenie_v_shinah = models.FloatField(
        verbose_name="Давление в шинах",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Ежедневные данные"
        verbose_name_plural = "Ежедневные данные"
        unique_together = ("car", "dt")  # Уникальная запись для машины и даты

    def __str__(self):
        return f"Данные для {self.car.id_car} на {self.dt}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        try:
            if not hasattr(self, "work_shift"):
                work_shift = WorkShift()
                work_shift.daily_data_id = self.id
                work_shift.save()
        except Exception as e:
            logging.info(f"Ошибка при создании обьекта WorkShift: {e}")


class WorkShift(models.Model):
    daily_data = models.OneToOneField(
        DailyData, on_delete=models.CASCADE, related_name="work_shift"
    )
    work_shift_name = models.CharField(
        default="",
        max_length=255,
        verbose_name="Смена",
        null=True,
        blank=True,
    )

    @staticmethod
    def get_shift_name(dt):
        if 8 <= dt.hour < 16:
            return "C1"
        elif 16 <= dt.hour:
            return "C2"
        else:
            return "C3"

    def save(self, *args, **kwargs):
        self.work_shift_name = self.get_shift_name(self.daily_data.dt)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Информация о смене: {self.id} - {self.work_shift_name} - daily_data_id: {self.daily_data.id}"


class SelectShift(models.Model):
    SELECT_SHIFT = [
        ("smena_one", "smena_one"),
        ("smena_two", "smena_two"),
        ("smena_three", "smena_three"),
        ("all", "all"),
    ]
    account_name = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    select_smena = models.CharField(
        max_length=20,
        verbose_name="Выбранная смена",
        choices=SELECT_SHIFT,
        default="all")

    def __str__(self):
        return f"Выбранная смена {self.select_smena}"
