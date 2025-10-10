# Selfinity Backend

Backend сервис на FastAPI с асинхронным доступом к PostgreSQL и миграциями Alembic.

## Запуск локально (без Docker)

1. Установите зависимости:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Создайте файл окружения:

   ```bash
   cp .env.example .env
   ```

   Отредактируйте `DATABASE_URL`, если требуется.

3. Запустите приложение:

   ```bash
   uvicorn app.main:app --reload
   ```

   Эндпоинт здоровья будет доступен по адресу `http://localhost:8000/health`.

## Запуск через Docker Compose

```bash
docker compose up --build
```

После запуска сервис доступен по `http://localhost:8000/health`. Для остановки используйте `docker compose down`.

## Миграции Alembic

Создание новой миграции:

```bash
alembic revision --autogenerate -m "my migration"
```

Применение миграций:

```bash
alembic upgrade head
```

## Тестирование

```bash
pytest
```

## Примеры запросов

```bash
curl http://localhost:8000/health
```

Ожидаемый ответ:

```json
{
  "status": "ok",
  "timestamp": "2025-10-10T15:06:00Z",
  "database": "connected"
}
```

