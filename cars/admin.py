from django.contrib import admin
from cars.models import Cars


class CarsAdmin(admin.ModelAdmin):
    list_display = (
        "id_car",
        "get_account_names",
        "toplivo",
    )

    def get_account_names(self, obj):
        return ", ".join([user.username for user in obj.account_name.all()])

    get_account_names.short_description = 'Пользователи'


admin.site.register(Cars, CarsAdmin)
