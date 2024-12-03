from django.shortcuts import render
from django.core.paginator import Paginator
from cars.models import Car


def car_list(request):
    cars = Car.objects.all()
    paginator = Paginator(cars, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'cars/index.html', {'page_obj': page_obj})
