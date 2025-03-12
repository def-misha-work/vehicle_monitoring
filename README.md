# vehicle_monitoring

### Run project

1) Создание вирт окружения
python3 -m venv .venv

2) Активация вирт окружения
Линукс:
source .venv/bin/activate
Виндоус:
source .venv/Scripts/activate

3) Абгрейд pip
python -m pip install --upgrade pip

4) Установка зависимостей
pip install -r requirements.txt

5) Старт проекта (добавить порты в зависимости настройки от сервера)
python manage.py runserver

6) Если postgres база не создана, накатить миграции
python manage.py makemigrations
python manage.py migrate



### Running dev
Run docker-compose

- To build: `make docker`
- To start: `docker compose -f ./docker-compose.yml up -d`
- To stop: `docker compose -f ./docker-compose.yml down`
- To clean-up data: `docker system prune -a --volumes --filter "label=io.confluent.docker"`
