## API для реферальной ссылки. Бэкенд на FastAPI.
### Структура проекта:
```python
referrerLink
├── alembic
│   ├── versions
│   │   ├── *файлы с версиями alembic*
│   ├── env.py
│   ├── README
│   └── script.py.mako
├── src
│   ├── certs # Нужно сгенерировать с помощью ssl
│   │   ├── private.pem
│   │   └── public.pem
│   ├── db
│   │   ├── config.py
│   │   └── models.py
│   ├── referralCode
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── utils.py
│   │   └── views.py
│   ├── users
│   │   ├── config.py
│   │   ├── main.py
│   │   └── utils.py
│   ├── config.py
│   ├── utils.py
│   └── main.py
├── .env # Нужно обязательно добавить для работы с базой данных (см. 3)
├── .gitignore
├── alembic.ini
├── poetry.lock
└── pyproject.toml

```
### 1) Запуск проекта
#### Зависимости
Стоит понимать что инициализация зависимостей происходит с помощью мен. зависимостей `poetry`. Если вы не пользуйтесь `poetry`, то придется устанавливать зависимости вручную.
А для тех у кого установлен `poetry` на глобальный интерпретатор, введите команду находясь в директории проекта:
```
poetry init
```

#### Миграции
Сделайте миграции с помощью `alembic`
```
alembic upgrade head
```

#### Запустите сервер с помощью файла `main.py`
```
python src/main.py
```


#### 
### 2) База данных
Данный проект лучше всего использовать с `postgresql`, так как там используется `UUID` в качестве первичного ключа.
### 3) ENV
```
DB_NAME=postgres
DB_PASSWORD=postgres
DB_USER=postgres
DB_HOST=localhost
DB_PORT=5432
```
