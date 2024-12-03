from django.contrib import admin
from cars.models import Car


class CarAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "updated_at",
        "car_number",
        "mileage",
        "fuel",
        "weight",
        "shift_day"
    )


admin.site.register(Car, CarAdmin)
