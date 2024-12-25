from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Jsession(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    jsession = models.CharField(
        unique=True,
        max_length=200
    )

    def __str__(self):
        return f"jsession: {self}"


class Car(TimestampMixin, models.Model):
    jsession = models.ForeignKey(
        Jsession,
        on_delete=models.CASCADE
    )
    car_number = models.IntegerField(
        verbose_name='Номер машины',
    )
    mileage = models.IntegerField(
        verbose_name='Пробег',
    )
    fuel = models.IntegerField(
        verbose_name='Расход топлива',
    )
    flight = models.IntegerField(
        verbose_name='Рейсы',
    )
    weight = models.IntegerField(
        verbose_name='Вес машины',
    )
    shift_day = models.IntegerField(
        verbose_name='Смена сутки г/т/км',
    )

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "car"
        verbose_name_plural = "cars"

    def __str__(self):
        return f"Информация по машине: {self.car_number}"
