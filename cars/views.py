from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    login as auth_login,
    logout as auth_logout
)
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from cars.models import Car


@login_required
def car_list(request):
    cars = Car.objects.all()
    paginator = Paginator(cars, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "cars/index.html", {"page_obj": page_obj})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('car_list')
        else:
            return render(
                request, "cars/login.html",
                {"error": "Неверный логин или пароль"}
            )
    return render(request, "cars/login.html")


def logout_view(request):
    auth_logout(request)
    return redirect('login')
