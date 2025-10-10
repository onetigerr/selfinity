# Фаза 1: Детальный пошаговый план

## Шаг 1.1: Инициализация FastAPI проекта

**Задача для Codex:**

Создай структуру FastAPI проекта со следующими требованиями:

- Python 3.11+
- FastAPI + uvicorn
- SQLAlchemy 2.0 + Alembic для миграций БД
- PostgreSQL через asyncpg
- pytest + pytest-asyncio для тестирования
- Структура папок:

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py         # FastAPI app
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py   # настройки приложения
│   │   └── database.py # подключение к БД
│   ├── api/
│   │   ├── __init__.py
│   │   └── health.py   # health-check endpoint
│   └── models/
│       └── __init__.py
├── tests/
│   ├── __init__.py
│   └── test_health.py
├── requirements.txt
├── pytest.ini
├── .env.example
└── README.md
```


Создай минимальный health-check endpoint GET /health который возвращает:

```json
{
  "status": "ok", 
  "timestamp": "2025-10-10T15:06:00Z"
}
```

Настрой конфигурацию через pydantic Settings для DATABASE_URL и других переменных.

## Шаг 1.2: Настройка PostgreSQL подключения

**Задача для Codex:**

Настрой подключение к PostgreSQL для проекта из предыдущего шага:

- Используй SQLAlchemy 2.0 с async/await
- Создай async engine и sessionmaker
- Настрой dependency для получения database session в FastAPI
- В config.py добавь DATABASE_URL из переменных окружения
- В database.py создай:
    - async engine
    - async_sessionmaker
    - get_db() dependency для внедрения сессии в endpoints
- Обнови health-check endpoint чтобы он проверял подключение к БД

Пример ожидаемого ответа health-check с БД:

```json
{
  "status": "ok",
  "timestamp": "2025-10-10T15:06:00Z", 
  "database": "connected"
}
```


## Шаг 1.3: Настройка Alembic для миграций

**Задача для Codex:**

Настрой Alembic для управления миграциями БД в проекте:

- Инициализируй alembic в корне backend/
- Настрой alembic.ini для работы с async PostgreSQL
- Настрой env.py для автогенерации миграций из SQLAlchemy моделей
- Создай первую миграцию "initial" которая создает пустую БД
- Убедись что команды работают:
    - alembic revision --autogenerate -m "initial"
    - alembic upgrade head

Структура должна стать:

```
backend/
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── alembic.ini
├── app/
│   └── ... (предыдущие файлы)
```


## Шаг 1.4: Настройка pytest с фикстурами

**Задача для Codex:**

Настрой pytest для тестирования FastAPI приложения:

- Создай conftest.py с основными фикстурами
- Фикстуры должны включать:
    - test_db: тестовая БД (используй SQLite in-memory или отдельную PostgreSQL БД)
    - client: TestClient для FastAPI app
    - async_client: AsyncClient для асинхронных тестов
- Создай test_health.py который тестирует health-check endpoint
- Тесты должны проверять:
    - GET /health возвращает 200
    - Ответ содержит правильную структуру JSON
    - Поле timestamp содержит валидную дату
    - Поле database равно "connected"

Убедись что pytest запускается и проходит все тесты.

## Шаг 1.5: Создание Docker Compose для локальной разработки

**Задача для Codex:**

Создай docker-compose.yml для локальной разработки:

- Сервис postgres:
    - PostgreSQL 15
    - База данных: lifebalance
    - Пользователь/пароль настраиваемые через env
    - Порт: 5432
    - Том для персистентности данных
- Сервис app:
    - Образ python:3.11-slim
    - Установка зависимостей из requirements.txt
    - Запуск uvicorn с hot reload
    - Проброс порта 8000
    - Переменные окружения для подключения к postgres
- Создай .env файл с примерами переменных
- Создай Dockerfile для backend (многоэтапная сборка опционально)

После docker-compose up приложение должно быть доступно на http://localhost:8000/health

## Шаг 1.6: Документация и финальная проверка

**Задача для codex:**

Подготовь финальную документацию и проверь работоспособность:

- Обнови README.md с инструкциями:
    - Как запустить проект локально
    - Как прогнать тесты
    - Как создать миграцию
    - Примеры curl запросов к health-check
- Создай .gitignore для Python проекта
- Проверь что FastAPI автоматически создает документацию на /docs и /redoc
- Добавь в health-check endpoint дополнительную информацию:
    - Версию приложения
    - Environment (development/production)

Итоговый ответ health-check:

```json
{
  "status": "ok",
  "timestamp": "2025-10-10T15:06:00Z",
  "database": "connected", 
  "version": "0.1.0",
  "environment": "development"
}
```


## Критерии завершения Фазы 1

После выполнения всех шагов у тебя должно получиться:

**Работающие команды:**

- `docker-compose up` - запускает приложение и БД
- `curl http://localhost:8000/health` - возвращает 200 OK с правильным JSON
- `pytest` - проходит все тесты
- `alembic upgrade head` - применяет миграции

**Доступные URL:**

- http://localhost:8000/health - health-check endpoint
- http://localhost:8000/docs - Swagger UI документация
- http://localhost:8000/redoc - ReDoc документация

**Файловая структура:**

- Все файлы созданы согласно структуре
- README.md содержит инструкции по запуску
- Тесты покрывают health-check функциональность
- Docker Compose поднимает все сервисы без ошибок

После этого можно переходить к Фазе 2 (пользователи и авторизация).
