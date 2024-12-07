from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Car(TimestampMixin, models.Model):
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
        return f"Номер машины: {self.car_number}"
