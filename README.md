[![Python](https://img.shields.io/badge/-Python_3.9.10-464646??style=flat-square&logo=Python)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/-Django-464646??style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django](https://img.shields.io/badge/-Django_rest_framework_3.12.4-464646??style=flat-square&logo=Django)](https://www.django-rest-framework.org)
<br>
# API для YaMDb

**_Командный учебный проект._**

## Описание:
Проект YaMDb собирает отзывы пользователей на произведения. 
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». 
Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). 
Пользователи могут оставлять комментарии к отзывам.
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.


## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/devlili/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

### Создание суперпользователя
Выполнить команду и следовать инструкциям:
```
python3 manage.py createsuperuser
```
После создания супепользователя можно использовать данные учетной записи для страницы администрирования - http://127.0.0.1:8000/admin/

## Документация к API

 После запуска dev-сервера документация к API доступна по адресу:
 http://127.0.0.1:8000/redoc/



## Авторы

- [Лилия Альмухаметова](https://github.com/devlili)
- [Андрей Хабаров](https://github.com/AndreyYP)
- [Елена Калинина](https://github.com/ElKalinina)

