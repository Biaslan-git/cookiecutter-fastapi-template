# Cookiecutter FastAPI Template

Простой и понятный шаблон для быстрого создания FastAPI проектов с современной архитектурой.

## Особенности

- [FastAPI](https://github.com/tiangolo/fastapi) с асинхронной поддержкой
- [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy) (async) для работы с БД
- [Alembic](https://github.com/sqlalchemy/alembic) (async) для миграций
- [Pydantic](https://github.com/pydantic/pydantic) для валидации
- Готовая настройка [uv](https://github.com/astral-sh/uv) (современный менеджер пакетов)
- Пример CRUD для пользователей
- Автоматическая настройка проекта после создания

## Требования

Перед использованием шаблона необходимо установить:

- **Python 3.11+** - [python.org](https://www.python.org/downloads/)
- **[uv](https://github.com/astral-sh/uv)** - современный менеджер пакетов Python
- **[cookiecutter](https://github.com/cookiecutter/cookiecutter)** - инструмент для создания проектов из шаблонов

## Быстрый старт

### 1. Создание проекта

```bash
# Из GitHub репозитория
cookiecutter https://github.com/Biaslan-git/cookiecutter-fastapi-template
```

Вам будет предложено ответить на несколько вопросов:

```
project_name [My FastAPI Project]: Мой Проект
project_slug [мой_проект]:
project_description [A FastAPI project]: Описание моего проекта
version [0.1.0]:
python_version [3.11]:
```

### 2. Автоматическая настройка

После создания проекта автоматически:

- Инициализируется uv проект
- Устанавливаются все зависимости
- Инициализируется и настраивается Alembic с async поддержкой
- Инициализируется git репозиторий

### 3. Дальнейшие шаги

```bash
cd your_project_name

# 1. Настройте .env файл
cp .env.example .env
# Отредактируйте .env по необходимости

# 2. Создайте первую миграцию
uv run alembic revision --autogenerate -m "Initial migration"

# 3. Примените миграции
uv run alembic upgrade head

# 4. Запустите сервер
uv run uvicorn main:app --reload
```

Откройте браузер:

- API документация (Swagger): <http://localhost:8000/docs>
- API документация (ReDoc): <http://localhost:8000/redoc>

## Структура созданного проекта

```
your_project/
├── main.py                 # Точка входа приложения
├── .env.example           # Пример конфигурации
├── pyproject.toml         # Зависимости проекта
├── alembic/               # Миграции базы данных
│   ├── env.py
│   └── versions/
└── app/
    ├── api/               # API endpoints (роуты)
    │   └── users.py       # Пример: endpoints для пользователей
    ├── core/              # Настройки приложения
    │   └── config.py      # Конфигурация из .env
    ├── dao/               # Data Access Objects (работа с БД)
    │   └── user.py        # Пример: DAO для пользователей
    ├── db/                # Настройка базы данных
    │   └── base.py        # SQLAlchemy Base и сессия
    ├── deps/              # Dependency Injection
    │   └── main.py        # Общие зависимости
    ├── models/            # SQLAlchemy модели
    │   └── user.py        # Пример: модель User
    ├── schemas/           # Pydantic схемы
    │   └── user.py        # Пример: схемы для User
    └── services/          # Бизнес-логика
        └── user.py        # Пример: сервис пользователей
```

## Примеры использования

### Пример API endpoint (уже включен)

```bash
# Получить список пользователей
curl http://localhost:8000/api/users/

# Создать пользователя
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "username": "testuser"}'
```

## Работа с базой данных

### Поддерживаемые БД

Измените `DATABASE_URL` в `.env`:

```bash
# SQLite (по умолчанию)
DATABASE_URL=sqlite+aiosqlite:///./app.db

# PostgreSQL
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname

# MySQL
DATABASE_URL=mysql+aiomysql://user:password@localhost:3306/dbname
```

### Миграции

```bash
# Создать новую миграцию
uv run alembic revision --autogenerate -m "Описание изменений"

# Применить миграции
uv run alembic upgrade head

# Откатить миграцию
uv run alembic downgrade -1

# Посмотреть историю
uv run alembic history
```

## Используемые технологии

- [FastAPI](https://github.com/tiangolo/fastapi) - современный веб-фреймворк
- [Uvicorn](https://github.com/encode/uvicorn) - ASGI сервер
- [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy) - ORM для работы с БД
- [Alembic](https://github.com/sqlalchemy/alembic) - миграции БД
- [Pydantic](https://github.com/pydantic/pydantic) - валидация данных
- [uv](https://github.com/astral-sh/uv) - менеджер пакетов
- [Ruff](https://github.com/astral-sh/ruff) - линтер и форматтер
- [pytest](https://github.com/pytest-dev/pytest) - фреймворк для тестирования

## Лицензия

MIT

## Помощь и поддержка

При возникновении проблем:

1. Проверьте версию Python: `python --version`
2. Проверьте установку uv: `uv --version`
3. Проверьте логи приложения
4. Создайте issue в [репозитории](https://github.com/Biaslan-git/cookiecutter-fastapi-template/issues)
