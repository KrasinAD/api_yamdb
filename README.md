# API_YAMDB

## **Описание проекта**
В проекте реализован интерфейс API, благодаря которому проект YaMDb собирает отзывы пользователей на произведения.

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

Запустить проект:

```
python manage.py runserver
```

## Как использовать

- Это приложение простое в использовании.
- Для аутентификации используются JWT-токены.
- Информация доступна как для незарегистрированных пользователей 
  (доступ к API только на чтение), так и для зарегистрированных.
- Исключение — эндпоинт /follow/: доступ к нему возможен только аутентифицированным пользователям.  
- Аутентифицированным пользователям разрешено изменение и удаление своего контента;
  в остальных случаях доступ предоставляется только для чтения.

## Примеры запросов и результаты:

*[GET ...api/v1/posts/](http://127.0.0.1:8000/api/v1/posts/)

**Результат:**
```
{
  "count": 123,
  "next": "http://api.example.org/accounts/?offset=400&limit=100",
  "previous": "http://api.example.org/accounts/?offset=200&limit=100",
  "results": [
    {
      "id": 0,
      "author": "string",
      "text": "string",
      "pub_date": "2021-10-14T20:41:29.648Z",
      "image": "string",
      "group": 0
    }
  ]
}
```

*[POST .../api/v1/posts/](http://127.0.0.1:8000/api/v1/posts/)

**Запрос:**
```
{
  "text": "string",
  "image": "string",
  "group": 0
}
```
**Результат:**
```
{
  "id": 0,
  "author": "string",
  "text": "string",
  "pub_date": "2019-08-24T14:15:22Z",
  "image": "string",
  "group": 0
}
```

*[GET ...api/v1/groups/](http://127.0.0.1:8000/api/v1/groups/)

**Результат:**
```
[
  {
    "id": 0,
    "title": "string",
    "slug": "string",
    "description": "string"
  }
]
```

*[GET ...api/v1/posts/{post_id}/comments/](http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/)

**Результат:**
```
[
  {
    "id": 0,
    "author": "string",
    "text": "string",
    "created": "2019-08-24T14:15:22Z",
    "post": 0
  }
]
```

*[POST ...api/v1/posts/{post_id}/comments/](http://127.0.0.1:8000/api/v1/posts/{post_id}/comments/)

**Запрос:**
```
{
  "text": "string"
}
```
**Результат:**
```
{
  "id": 0,
  "author": "string",
  "text": "string",
  "created": "2019-08-24T14:15:22Z",
  "post": 0
}
```

*[GET ...api/v1/follow/](http://127.0.0.1:8000/api/v1/follow/)

**Результат:**
```
[
  {
    "user": "string",
    "following": "string"
  }
]
```

*[POST ...api/v1/follow/](http://127.0.0.1:8000/api/v1/follow/)

**Запрос:**
```
{
  "following": "string"
}
```
**Результат:**
```
{
  "user": "string",
  "following": "string"
}
```

#### Более подробное описание API можно получить по адресу:
http://127.0.0.1:8000/redoc/
***

### Автор проекта

- [@KrasinAD](https://github.com/KrasinAD)