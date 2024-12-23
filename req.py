import requests


URL_LOGIN = "http://s1.mdvr.kz:88/StandardApiAction_login.action"
ACCOUNT = "?account="
PASSWORD = "&password="
USER_LOGIN = "test"
USER_PASSWORD = "181023"
URL_GET_ENTER = URL_LOGIN + ACCOUNT + USER_LOGIN + PASSWORD + USER_PASSWORD


response = requests.get(URL_GET_ENTER)
data = response.json()
print(response.status_code)
print(data["jsession"])
