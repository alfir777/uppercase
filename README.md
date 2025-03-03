# Тестовое задание

## Запуск

1. Клонировать репозиторий или форк

```
git clone https://github.com/alfir777/uppercase.git
```

2. Запустить локально

```
cd uppercase/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd src/
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

3. (Опционально) Вместо pip использовать poetry

```
poetry install --no-root --only main
```

4. Или развернуть контейнер с помощью в docker-compose (https://docs.docker.com/compose/install/)

```
docker compose up -d
docker exec -it uppercase-api python manage.py createsuperuser
```

5. Перейти по адресу http://localhost:8000/