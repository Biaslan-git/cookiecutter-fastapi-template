# {{cookiecutter.project_name}}

{{cookiecutter.project_description}}

## Требования

- Python {{cookiecutter.python_version}}+
- uv (package manager)

## Установка
```bash
# Создать .env файл
cp .env.example .env

# Применить миграции
uv run alembic upgrade head

# Запустить сервер
uv run uvicorn app.main:app --reload
```

## Структура проекта
```
app/
├── models/       # Бизнес-сущности
├── schemas/      # Pydantic схемы
├── services/     # Бизнес-логика
├── crud/         # CRUD операции
├── db/           # SQLAlchemy (async)
└── api/          # FastAPI routes
```

## API Документация

После запуска доступна по адресу:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
