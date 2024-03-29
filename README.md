# API_YAMDB

## **Описание проекта**
В проекте реализован интерфейс API, благодаря которому проект YaMDb собирает отзывы пользователей на произведения.
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

## Как запустить проект на Windows:

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/Scripts/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Загрузите тестовые данные в БД:

```
python manage.py load
```

Запустить проект:

```
python manage.py runserver
```

## Ресурсы API YaMDb

- Ресурс auth: аутентификация.
- Ресурс users: пользователи.
- Ресурс titles: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
- Ресурс categories: категории (типы) произведений («Фильмы», «Книги», «Музыка»). Одно произведение может быть привязано только к одной категории.
- Ресурс genres: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
- Ресурс reviews: отзывы на произведения. Отзыв привязан к определённому произведению.
- Ресурс comments: комментарии к отзывам. Комментарий привязан к определённому отзыву.
- Каждый ресурс описан в документации: указаны эндпоинты (адреса, по которым можно сделать запрос), разрешённые типы запросов, права доступа и дополнительные параметры, когда это необходимо.

## Как использовать:
### Алгоритм регистрация новых пользователей:
1. Пользователь отправляет POST-запрос с параметрами ```email``` и ```username``` на эндпоинт ```/api/v1/auth/signup/```.
2. Сервис YaMDB отправляет письмо с кодом подтверждения (```confirmation_code```) на указанный адрес ```email```.
3. Пользователь отправляет POST-запрос с параметрами ```username``` и ```confirmation_code``` на эндпоинт ```/api/v1/auth/token/```, в ответе на запрос ему приходит ```token (JWT-токен)```.
В результате пользователь получает токен и может работать с API проекта, отправляя этот токен с каждым запросом. 
После регистрации и получения токена пользователь может отправить PATCH-запрос на эндпоинт ```/api/v1/users/me/``` и заполнить поля в своём профайле (описание полей — в документации).

### Пользовательские роли:
* Аноним — может просматривать описания произведений, читать отзывы и комментарии.
* Аутентифицированный пользователь (```user```) — может, как и Аноним, читать всё, дополнительно он может публиковать отзывы и ставить оценку произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы; может редактировать и удалять свои отзывы и комментарии. Эта роль присваивается по умолчанию каждому новому пользователю.
* Модератор (```moderator```) — те же права, что и у Аутентифицированного пользователя плюс право удалять любые отзывы и комментарии.
* Администратор (```admin```) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
* Суперюзер Django — обладет правами администратора (```admin```)

## Примеры запросов и результаты:

**Регистрация нового пользователя**

[POST .../auth/signup/](http://127.0.0.1:8000/api/v1/auth/signup/)

**Запрос:**
```
{
  "email": "user@example.com",
  "username": "string"
}
```

**Результат:**
```
{
  "email": "string",
  "username": "string"
}
```
**Получение JWT-токена**

[POST .../auth/token/](http://127.0.0.1:8000/api/v1/auth/token/)

**Запрос:**
```
{
  "username": "string",
  "confirmation_code": "string"
}
```
**Результат:**
```
{
  "token": "string"
}
```
**Получение списка всех категорий**

[GET .../categories/](http://127.0.0.1:8000/api/v1/categories/)

**Результат:**
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "name": "string",
      "slug": "string"
    }
  ]
}
```

[POST .../categories/](http://127.0.0.1:8000/api/v1/categories/)

**Запрос:**
```
{
  "name": "string",
  "slug": "string"
}
```
**Результат:**
```
{
  "name": "string",
  "slug": "string"
}
```

**Категории жанров**

[GET .../genres/](http://127.0.0.1:8000/api/v1/genres/)

**Результат:**
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "name": "string",
      "slug": "string"
    }
  ]
}
```

[POST .../genres/](http://127.0.0.1:8000/api/v1/genres/)

**Запрос:**
```
{
  "name": "string",
  "slug": "string"
}
```
**Результат:**
```
{
  "name": "string",
  "slug": "string"
}
```
**Произведения, к которым пишут отзывы (определённый фильм, книга или песенка).**

*[GET .../titles/](http://127.0.0.1:8000/api/v1/titles/)

**Результат:**
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "name": "string",
      "year": 0,
      "rating": 0,
      "description": "string",
      "genre": [
        {
          "name": "string",
          "slug": "string"
        }
      ],
      "category": {
        "name": "string",
        "slug": "string"
      }
    }
  ]
}
```

*[POST .../titles/](http://127.0.0.1:8000/api/v1/titles/)

**Запрос:**
```
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```
**Результат:**
```
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```

#### Более подробное описание API можно получить по адресу:
http://127.0.0.1:8000/redoc/
***

### Авторы проекта:

- [@KrasinAD](https://github.com/KrasinAD)
- [@Erinnerungen](https://github.com/Erinnerungen)
- [@shustrov19](https://github.com/shustrov19)