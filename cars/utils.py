# import requests

# import json
import requests

from constants import (
    # URL_GET_JSESSION,
    URL_GET_TECH,
    URL_GET_FUEL,
    # URL_GET_WEIGHT,
)


def get_request(url, **params):
    """
    Выполняет GET-запрос к указанному URL с переданными GET-параметрами.
    :param url: URL для запроса
    :param params: Произвольное количество GET-параметров
    :return: Ответ сервера
    """
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Проверка на ошибки HTTP
        return response.json()  # Возвращаем ответ в формате JSON
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при выполнении запроса: {e}")
        return None


def get_tech(jsession: str):
    result = get_request(URL_GET_TECH, jsession=jsession)
    vehicles_dict: dict = result["vehicles"]
    vehicle_ids: list = [vehicle["id"] for vehicle in vehicles_dict]
    devidno: list = []
    for vehicle in vehicles_dict:
        if "dl" in vehicle:
            for dl_item in vehicle["dl"]:
                devidno.append(dl_item["id"])
    return vehicle_ids, devidno


if __name__ == "__main__":
    jsession = 'c4bf8a154c894f1abb72a73d17cd7ea9'
    vehicle_ids, devidno = get_tech(jsession)
    print(vehicle_ids)
    print(devidno)
    fuel_yl: list = []
    mileage_lc: list = []
    for item in devidno:
        result = get_request(
            URL_GET_FUEL,
            jsession=jsession,
            devIdno=item
        )
        for item in result['status']:
            # / 100 получаем литры
            fuel_yl.append(item["yl"] / 100)
            # / 1000 получаем километры
            mileage_lc.append(item["lc"] / 1000)
    print(fuel_yl)
    print(mileage_lc)
