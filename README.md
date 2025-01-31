[![Main foodgram workflow](https://github.com/SoulScavenger/foodgram/actions/workflows/main.yml/badge.svg)](https://github.com/SoulScavenger/foodgram/actions/workflows/main.yml)

### Описание проекта
Проект представляет собой веб-приложения для публикации рецептов.

### Стек технологий
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/Django-0b990f?style=for-the-badge&logo=django&logoColor=ffffff)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-0352fc?style=for-the-badge&logo=PostgreSQL&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-032cfc?style=for-the-badge&logo=Docker&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-07fc03?style=for-the-badge&logo=nginx&logoColor=white)
![Gunicorn](https://img.shields.io/badge/Gunicorn-03fcf?style=for-the-badge&logo=Gunicorn&logoColor=white)
![React](https://img.shields.io/badge/React-03ebfc?style=for-the-badge&logo=React&logoColor=white)


### Пример сайта
[Пример сайта](https://soulscavengerkitty.ddns.net/)

### API документация

[API документация](https://soulscavengerkitty.ddns.net/api/docs/)



### Как запустить проект:
#### Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/SoulScavenger/foodgram.git
```

```
cd foodgram
```

#### Создать в корневой директории проекта файл .env и добавить следующие переменные:

##### Переменные которые необходимо указать в .env:
```
SECRET_KEY
DEBUG
ALLOWED_HOSTS
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
HOST
PORT
```

#### Запустить Docker Compose:

Под Windows:
```
docker compose docker-compose.production.yml up
```

Под Linux:
```
sudo docker compose -f docker-compose.production.yml up -d
```

#### Выполнить миграции:

Под Windows:
```
docker compose docker-compose.production.yml exec backend python manage.py migrate

docker compose docker-compose.production.yml exec backend python manage.py collectstatic

docker compose docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/static/
```

Под Linux:
```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate

sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic

sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/static/
```

#### Заполнить базу данных:
Под Windows:
```
docker compose docker-compose.production.yml exec backend python manage.py fill_db
```
Под Linix:
```
sudo docker compose docker-compose.production.yml exec backend python manage.py fill_db
```

### Автор
#### Maksim Torgashin