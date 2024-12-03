# Generated by Django 5.1.3 on 2024-12-03 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Car",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("car_number", models.IntegerField(verbose_name="Номер машины")),
                ("mileage", models.IntegerField(verbose_name="Пробег")),
                ("fuel", models.IntegerField(verbose_name="Расход топлива")),
                ("weight", models.IntegerField(verbose_name="Вес машины")),
                ("shift_day", models.IntegerField(verbose_name="Смена сутки г/т/км")),
            ],
            options={
                "verbose_name": "car",
                "verbose_name_plural": "cars",
                "ordering": ("-created_at",),
            },
        ),
    ]