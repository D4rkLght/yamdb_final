![yamdb_workflow](https://github.com/D4rkLght/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
### Стек технологий
[![Python](https://img.shields.io/badge/-Python-464641?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-464646?style=flat-square&logo=django)](https://www.djangoproject.com/)
[![Pytest](https://img.shields.io/badge/Pytest-464646?style=flat-square&logo=pytest)](https://docs.pytest.org/en/6.2.x/)
[![Docker](https://img.shields.io/badge/Docker-464646?style=flat-square&logo=docker)](https://hub.docker.com/)
[![Postgresql](https://img.shields.io/badge/Postgres-464646?style=flat-square&logo=POSTGRESQL)](https://www.postgresql.org/)

# Проект YaMDb
Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен администратором (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая сюита Баха.
Произведению может быть присвоен жанр (Genre) из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы (Review) и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

### Установка:
Создайте директорию infra/:
~~~
mkdir infra
~~~
В директории создать файл infra/.env и наполнить: 
- DB_ENGINE=django.db.backends.postgresql
- DB_NAME= # название дб
- POSTGRES_USER= # имя пользователя
- POSTGRES_PASSWORD= # пароль
- DB_HOST=db
- DB_PORT=5432

Из папки infra/ соберите образ:
```
docker-compose up -d
```
Миграции:
```
docker-compose exec web python manage.py migrate
```
Сбор статики:
```
docker-compose exec web python manage.py collectstatic --no-input
```
Создание суперюзера:
```
docker-compose exec web python manage.py createsuperuser
```
Резервная копия:
```
docker-compose exec web python manage.py dumpdata > fixtures.json 
```

## Над проектом работали:
1. Разработчик [Анастасия Хоменко](https://github.com/k4omenkoanastasia) писала всю часть, касающуюся управления пользователями (Auth и Users): систему регистрации и аутентификации, права доступа, работу с JWT токеном, систему подтверждения через e-mail, и файл READMЕ<br>


2. Разработчик [Алексей Антипов ](https://github.com/FlynnFNX) писал категории (Categories), жанры (Genres) и произведения (Titles): модели, представления и эндпойнты для них.<br>

3. Разработчик и Тимлид [Ярослав Андреев ](https://github.com/D4rkLght) занимался отзывами (Review) и комментариями (Comments): описывает модели, представления, настраивал эндпойнты, определял права доступа для запросов, рейтингами произведений.
