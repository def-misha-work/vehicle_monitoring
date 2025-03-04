import logging
import time
from datetime import datetime
from functools import wraps
from typing import Any, Callable, Optional, Tuple

import pytz
import requests
from cryptography.fernet import Fernet

from cars.constants import URL_GET_FUEL  # URL_GET_JSESSION,
from cars.constants import KEY, URL_GET_TECH, URL_GET_WEIGHT


def encrypt_password(password):
    fernet = Fernet(KEY)
    return fernet.encrypt(password.encode()).decode()


def decrypt_password(encrypted_password):
    fernet = Fernet(KEY)
    return fernet.decrypt(encrypted_password.encode()).decode()


def time_it(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(
            f"Функция '{func.__name__}'" f" выполнена за {execution_time:.4f} секунд."
        )
        return result

    return wrapper


def get_day_start_end():
    """
    Получаем начало и конец текущего дня.
    Устанавливаем временную зону для Москвы.
    """
    moscow_tz = pytz.timezone("Europe/Moscow")
    now = datetime.now(moscow_tz)
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)
    formatted_start = start_of_day.strftime("%Y-%m-%d %H:%M:%S")
    formatted_end = end_of_day.strftime("%Y-%m-%d %H:%M:%S")
    return (formatted_start.replace(" ", "%20"), formatted_end.replace(" ", "%20"))


def get_request(url: str, **params: str) -> Optional[dict]:
    """
    Выполняет GET-запрос.
    """
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.info(f"Ошибка при выполнении запроса: {e}")
        return None


@time_it
def get_tech(jsession: str) -> Optional[Tuple[list[int], list[int]]]:
    """
    Получаем данные по технике.
    """
    result: dict = get_request(URL_GET_TECH, jsession=jsession)
    # Проверяем, есть ли ключ "message" в ответе
    if "message" in result:
        return False
    # Проверяем, есть ли ключ "vehicles" в ответе
    if "vehicles" not in result:
        return False

    vehicles_dict: dict = result["vehicles"]
    devidno: list = []
    for vehicle in vehicles_dict:
        if "dl" in vehicle:
            for dl_item in vehicle["dl"]:
                devidno.append(dl_item["id"])
    return devidno


@time_it
def get_fuel_and_mileage(
    jsession: str, devidno: list[int]
) -> Optional[Tuple[list[int], list[int]]]:
    """
    Получаем данные по топливу и пробегу.
    """
    fuel_yl: list = []
    mileage_lc: list = []
    for item in devidno:
        result = get_request(URL_GET_FUEL, jsession=jsession, devIdno=item)
        if "message" in result:
            return False
        if "status" not in result:
            return False
        for item in result["status"]:
            # / 100 получаем литры
            fuel_yl.append(item["yl"] / 100)
            # / 1000 получаем километры
            mileage_lc.append(item["lc"] / 1000)
    return fuel_yl, mileage_lc


@time_it
def get_weight(
    jsession: str,
    devidno: list[int],
) -> Optional[list[int]]:
    """
    Получаем вес в кг.
    """
    weight_p2: list = []
    begintime, endtime = get_day_start_end()
    for item in devidno:
        result = get_request(
            URL_GET_WEIGHT,
            jsession=jsession,
            devIdno=item,
            begintime=begintime,
            endtime=endtime,
        )
        if "message" in result:
            return False
        if "status" not in result:
            return False
        for item in result["status"]:
            weight_p2.append(item["p2"])
    return weight_p2


if __name__ == "__main__":
    # заглушка на авторизацию
    jsession = "c4bf8a154c894f1abb72a73d17cd7ea9"

    # Получаем технику
    result = get_tech(jsession)
    if result is False:
        # TODO тут вернуть шаблон, что не получилось получить данные
        logging.info("Тут будет возврат шаблона")
    else:
        vehicle_ids, devidno = result
    logging.info(vehicle_ids)
    logging.info(devidno)

    # Получаю топливо и пробег
    result = get_fuel_and_mileage(jsession, devidno)
    if result is False:
        # TODO тут вернуть шаблон, что не получилось получить данные
        logging.info("Тут будет возврат шаблона")
    fuel_yl, mileage_lc = result
    logging.info(fuel_yl)
    logging.info(mileage_lc)
