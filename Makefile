env:
	@echo "Create env"
	python3 -m venv .venv
install:
	@echo "Install"
	python -m ensurepip --upgrade
	python -m pip install --upgrade setuptools
	pip install -r requirements.txt

run:
	@echo "Run"
	python manage.py runserver 0.0.0.0:8080

lint:
	@echo "Start lint"
	black .

isort:
	@echo "Start isort"
	isort .

format: lint isort
	@echo "Format Done"

docker:
	@echo "Docker build"
	docker -l info build -t vehicle_monitoring:latest .

