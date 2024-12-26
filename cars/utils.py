import requests
import logging

from typing import Optional, Tuple
from cars.constants import (
    # URL_GET_JSESSION,
    URL_GET_TECH,
    URL_GET_FUEL,
    # URL_GET_WEIGHT,
)


def get_request(url: str, **params: str) -> Optional[dict]:
    """
    Выполняет GET-запрос к указанному URL с переданными GET-параметрами.
    :param url: URL для запроса.
    :param params: Произвольное количество GET-параметров.
    :return: Ответ сервера.
    """
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Проверка на ошибки HTTP
        return response.json()  # Возвращаем ответ в формате JSON
    except requests.exceptions.RequestException as e:
        logging.info(f"Ошибка при выполнении запроса: {e}")
        return None


def get_tech(
    jsession: str
) -> Optional[Tuple[list[int], list[int]]]:
    """
    Получаем данные по технике.
    """
    result: dict = get_request(URL_GET_TECH, jsession=jsession)
    if not result:
        return False
    vehicles_dict: dict = result["vehicles"]
    vehicle_ids: list = [vehicle["id"] for vehicle in vehicles_dict]
    devidno: list = []
    for vehicle in vehicles_dict:
        if "dl" in vehicle:
            for dl_item in vehicle["dl"]:
                devidno.append(dl_item["id"])
    return vehicle_ids, devidno


def get_fuel_and_mileage(
    jsession: str,
    devidno: list[int]
) -> Optional[Tuple[list[int], list[int]]]:
    """
    Получаем данные по топливу и пробегу.
    """
    fuel_yl: list = []
    mileage_lc: list = []
    for item in devidno:
        result = get_request(
            URL_GET_FUEL,
            jsession=jsession,
            devIdno=item
        )
        if not result:
            return False
        for item in result['status']:
            # / 100 получаем литры
            fuel_yl.append(item["yl"] / 100)
            # / 1000 получаем километры
            mileage_lc.append(item["lc"] / 1000)
    return fuel_yl, mileage_lc


if __name__ == "__main__":
    # заглушка на авторизацию
    jsession = 'c4bf8a154c894f1abb72a73d17cd7ea9'

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
