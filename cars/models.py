from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


User = get_user_model()


class UserPassword(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="encrypted_password"
    )
    encrypted_password = models.CharField(max_length=255)


class Jsession(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="jsession"
    )
    jsession = models.CharField(max_length=255)

    def __str__(self):
        return f"jsession: {self.jsession}"


class Toplivo(models.Model):
    dt = models.DateTimeField(default=timezone.now)
    ostatok_na_tekushchii_moment = models.FloatField()
    raskhod_za_period = models.FloatField()
    raskhod_za_poezdku = models.FloatField()
    raskhod_na_khkh_za_period = models.FloatField()
    raskhod_pod_nagruzkoi_za_period = models.FloatField()
    raskhod_v_puti_za_period = models.FloatField()
    raskhod_privedennii_g_t_km_za_period = models.FloatField()
    raskhod_privedennii_g_t_km_obshchii = models.FloatField()


class DatchikVesa(models.Model):
    dt = models.DateTimeField(default=timezone.now)
    tekushchaya_nagruzka = models.FloatField()
    summarnii_ves_za_period = models.FloatField()
    min_ves_za_period = models.FloatField()
    max_ves_za_period = models.FloatField()
    srednii_ves_reisa_za_period = models.FloatField()


class Probeg(models.Model):
    dt = models.DateTimeField(default=timezone.now)
    probeg_na_segodnya = models.FloatField()
    probeg_za_period = models.FloatField()
    kolichestvo_reisov = models.FloatField()
    kolichestvo_poezdok_za_period = models.FloatField()


class Vremya(models.Model):
    dt = models.DateTimeField(default=timezone.now)
    vremya_s_nachala_perioda = models.FloatField()
    vremya_raboty_dvigatelya_za_period = models.FloatField()
    vremya_hkh_za_period = models.FloatField()
    motochasy_obshchie = models.FloatField()
    motochasy_za_period = models.FloatField()


class Shini(models.Model):
    dt = models.DateTimeField(default=timezone.now)
    davlenie_v_shinah = models.FloatField()


class Cars(models.Model):
    dt = models.DateTimeField(default=timezone.now)
    id_car = models.CharField(
        max_length=255,
        unique=True,
    )
    account_name = models.ManyToManyField(
        User,
        related_name="cars",
        verbose_name="Пользователи",
        blank=True,
    )
    toplivo = models.ForeignKey(
        Toplivo,
        related_name="cars",
        verbose_name="Топливо",
        on_delete=models.CASCADE,
        null=True,
    )
    datchik_vesa = models.ForeignKey(
        DatchikVesa,
        related_name="cars",
        verbose_name="Датчик веса",
        on_delete=models.CASCADE,
        null=True,
    )
    probeg = models.ForeignKey(
        Probeg,
        related_name="cars",
        verbose_name="Пробег",
        on_delete=models.CASCADE,
        null=True,
    )
    vremya = models.ForeignKey(
        Vremya,
        related_name="cars",
        verbose_name="Время",
        on_delete=models.CASCADE,
        null=True,
    )
    shini = models.ForeignKey(
        Shini,
        related_name="cars",
        verbose_name="Давление в шинах",
        on_delete=models.CASCADE,
        null=True,
    )

    class Meta:
        verbose_name = "car"
        verbose_name_plural = "cars"

    def __str__(self):
        return f"Информация по машине: {self.id_car}"
