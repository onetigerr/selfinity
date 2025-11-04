# Гайд по проверке Фазы 2

Этот документ помогает убедиться, что реализованы все задачи Фазы 2: от модели пользователя до UI-форм и docker-compose.

## Что сделано в фазе 2

- **Бэкенд**: модель `User`, async-репозиторий, `AuthService`, JWT/хеширование (`app/core/security.py`), зависимости (`app/api/deps.py`) и роутер `/auth` с методами `register/login/me/refresh/logout`.
- **API**: все эндпоинты работают с JWT Bearer, присутствует проверка токена и обработка ошибок через HTTPException.
- **Тесты**: юнит-тесты `tests/test_auth.py` и интеграционные `tests/test_integration_auth.py`, фикстуры создают/чистят схему БД автоматически.
- **Фронтенд**: Vite+React+TypeScript проект (`frontend/`), формы регистрации/входа, контекст авторизации, защищённый роут профиля, API-клиент с интерцептором, хранение токена в `localStorage`.
- **Инфраструктура**: docker-compose поднимает `postgres`, `redis`, `backend`, `frontend`, hot reload доступен для обоих сервисов; добавлен демонстрационный скрипт `backend/scripts/demo_auth.sh`.

## 1. Предварительные требования

- Python 3.12+
- PostgreSQL (рекомендуется) или SQLite для быстрого прогона
- Инструменты для виртуального окружения (`venv`, `pyenv` и т. п.)

Все команды ниже предполагают, что текущая директория — `backend/`.

## 2. Установка зависимостей

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 3. Настройка переменной `DATABASE_URL`

Укажите базу, с которой будет работать Alembic. Пример для PostgreSQL:

```bash
export DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/lifebalance"
```

Для быстрого smoke-теста можно использовать SQLite:

```bash
export DATABASE_URL="sqlite+aiosqlite:///./phase2.db"
```

> Нужна отдельная база? Создайте её вручную (например, `createdb my_db` или `psql -c "CREATE DATABASE my_db;"`) и подставьте своё имя в `DATABASE_URL`.

### Если работаете через Docker

1. Убедитесь, что `docker` и `docker compose` установлены (на macOS и Windows это Docker Desktop, на Linux — Docker Engine + compose plugin).
2. Поднимите окружение проекта (минимум `postgres` и `backend`):
   ```bash
   docker compose up -d postgres backend
   ```
   Для фронтенда добавьте `frontend` к списку сервисов.
3. Проверьте статус сервисов:
   ```bash
   docker compose ps
   ```
   Обратите внимание, что сервис бэкенда называется `backend`.
4. Зайдите внутрь контейнера приложения:
   ```bash
   docker compose exec backend bash
   ```
   Если контейнер не запущен, поднимите его командой `docker compose up -d backend`.
5. Внутри контейнера экспортируйте переменную и запустите миграцию:
   ```bash
   export DATABASE_URL="postgresql+asyncpg://postgres:postgres@postgres:5432/lifebalance"
   alembic upgrade head
   ```
   Здесь `postgres` в URL — имя контейнера базы, указанное в `docker-compose.yml`. Создавать базу вручную не нужно: compose поднимет PostgreSQL с параметрами из конфигурации.
6. После завершения можно выйти из контейнера (`exit`). Перезагружать сервисы не требуется; достаточно одного запуска миграций.

## 4. Запуск миграции Alembic

```bash
alembic upgrade head
```

После выполнения команды должна появиться таблица `users` со столбцами `id`, `email`, `password_hash`, `language_preference`, `created_at`, `updated_at`, а также перечисление `language_preference_enum` со значениями `ru` и `en`.

Проверить результат можно любым клиентом (например, `psql`, `sqlite3` или отдельным скриптом).

## 5. Проверка auth API

После применения миграций можно протестировать основные эндпоинты аутентификации.

### Регистрация

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "demo@example.com", "password": "secret123"}'
```

Ожидаемый ответ: данные пользователя с полями `id`, `email`, `language_preference`, `created_at`.

### Логин и получение токена

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "demo@example.com", "password": "secret123"}'
```

Ответ содержит `access_token` и `token_type`. Сохраните токен в переменную:

```bash
TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "demo@example.com", "password": "secret123"}' | jq -r '.access_token')
```

### Получение профиля

```bash
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/auth/me
```

Если токен валиден, вернётся профиль пользователя. Без заголовка `Authorization` сервис отвечает `401 Not authenticated`.

### Обновление токена

```bash
curl -X POST http://localhost:8000/auth/refresh \
  -H "Authorization: Bearer $TOKEN"
```

Ответ: новый `access_token`, который можно сохранить и переиспользовать.

### Выход

```bash
curl -X POST http://localhost:8000/auth/logout \
  -H "Authorization: Bearer $TOKEN" -i
```

Ответ: статус `204 No Content`. На стороне сервера дополнительное состояние пока не хранится — достаточно стереть токен на клиенте.

## 6. Просмотр модели (опционально)

Можно запустить Python, чтобы убедиться, что модель доступна из ORM:

```bash
python
```

```python
from app.core.database import get_session_factory
from app.models import User

session_factory = get_session_factory()
async def show_tables():
    async with session_factory() as session:
        result = await session.execute("SELECT name FROM sqlite_master WHERE type='table';")
        print(result.all())
```

## 7. Прогон тестов

```bash
pytest
```

Тестовый набор включает:

- `tests/test_auth.py` — unit-сценарии регистрации, логина, `/auth/me`.
- `tests/test_integration_auth.py` — end-to-end сценарии полного флоу, refresh и logout.

Запускаем `pytest` либо выборочно `pytest -k auth`. Перед стартом обновите зависимости `pip install -r requirements.txt` (добавлены `passlib[bcrypt]`, `python-jose[cryptography]`).

## 8. Откат миграции (опционально)

Чтобы вернуть состояние к начальному:

```bash
alembic downgrade base
```

Команда удалит таблицу `users` и соответствующий enum.

## 9. Запуск фронтенда

Перейдите в директорию `frontend/` и установите зависимости:

```bash
cd ../frontend
npm install
```

Создайте локальный файл окружения (при необходимости):

```bash
cp .env.example .env.local  # можно изменить VITE_API_URL при разработке
```

Запустите dev-сервер:

```bash
npm run dev
```

Приложение будет доступно на `http://localhost:5173`. Формы регистрации и входа располагаются на `/register` и `/login`, защищённая страница профиля — на `/profile`.

### Структура фронтенда

- `src/api/` — `apiClient.ts` с axios-интерцептором и `authApi.ts` с методами `register/login/me/refresh/logout`.
- `src/context/AuthContext.tsx` — хранит пользователя, токен и операции (`login`, `register`, `logout`, `refreshProfile`).
- `src/components/LoginForm.tsx` / `RegisterForm.tsx` — формы на базе React Hook Form.
- `src/pages/` — `LoginPage`, `RegisterPage`, `ProfilePage`, `ProtectedRoute`.
- `src/App.tsx` — маршрутизация и редиректы.

### Как проверить UI

1. Перейдите на `/register`, заполните email/пароль (минимум 6 символов). После успешной регистрации произойдёт редирект на `/profile`.
2. На `/profile` отобразится email и локализация пользователя; кнопка «Выйти» очищает токен и возвращает на `/login`.
3. При попытке открыть `/profile` без токена произойдёт редирект на `/login`.
4. Повторная регистрация с тем же email возвращает ошибку, которую можно увидеть в DevTools (400 «Email already registered»).

## 10. Docker Compose (быстрый старт)

В каталоге `backend/` доступен `docker-compose.yml`, который поднимает четыре сервиса: `postgres`, `redis`, `backend`, `frontend`.

1. Соберите и запустите стек:
   ```bash
   docker compose up -d --build
   ```
2. Бэкенд доступен на `http://localhost:8000`, фронтенд — на `http://localhost:5173`.
3. Для выполнения миграций и управления зависимостями используйте команды вида `docker compose exec backend <command>`.

> Во фронтенд-контейнер монтируется директория проекта, поэтому поддерживается hot reload. Анонимный том `/app/node_modules` предотвращает конфликт с локальными зависимостями.
> Значения переменных берутся из `backend/.env` и `frontend/.env`. При необходимости укажите другой `VITE_API_URL` или `DATABASE_URL` до запуска compose.

## 11. Скрипт демонстрации API

В `backend/scripts/demo_auth.sh` находится пример автоматизированного сценария, покрывающего регистрацию → логин → обновление токена → запрос профиля → выход. Перед запуском убедитесь, что установлен `jq`.

```bash
cd backend
API_URL=http://localhost:8000 ./scripts/demo_auth.sh
```

Переменные `EMAIL` и `PASSWORD` можно переопределить через окружение.

---

После прохождения шагов выше вы подтвердите готовность базовой части Фазы 2 (модель пользователя + миграция). Дальнейшие задачи описаны в `doc/phase-2.md`.
