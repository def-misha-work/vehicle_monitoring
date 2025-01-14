import os

from dotenv import load_dotenv

load_dotenv()

DOMEN = os.getenv("DOMEN")
URL_GET_JSESSION = DOMEN + "StandardApiAction_login.action"
URL_GET_TECH = DOMEN + "StandardApiAction_queryUserVehicle.action"
URL_GET_FUEL = DOMEN + "StandardApiAction_getDeviceStatus.action"
URL_GET_WEIGHT = DOMEN + "StandardApiAction_getDeviceStatus.action"
KEY = os.getenv("KEY").encode()

# 2024-12-22%2000:00:00
# USER_LOGIN = "test"
# USER_PASSWORD = "181023"
# USER_PASSWORD = "222"
