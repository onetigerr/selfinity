# Фаза 2 — Проверка реализованной аутентификации (Backend)

Этот документ описывает, как локально проверить реализованные в этой фазе изменения: регистрацию, логин и получение данных текущего пользователя на FastAPI бэкенде.

## Что реализовано

- Хеширование паролей и JWT:
  - `backend/app/core/security.py`
- Репозиторий пользователей (async SQLAlchemy 2.0):
  - `backend/app/repositories/user_repository.py`
- Сервис аутентификации:
  - `backend/app/services/auth_service.py`
- Зависимости для извлечения текущего пользователя:
  - `backend/app/api/deps.py`
- Роутер аутентификации (`/auth`):
  - `backend/app/api/auth.py`
- Подключение CORS и роутера в приложении:
  - `backend/app/main.py`
- Тесты API аутентификации:
  - `backend/tests/test_auth.py`

## Предварительные требования

- Python 3.12+
- Виртуальное окружение (`venv`, `pyenv`) или Docker (опционально)
- PostgreSQL 15+ (локально или через Docker Compose)

## Установка зависимостей

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Настройка окружения

1) Проверьте файл `backend/.env`. Необходимые переменные уже добавлены:

- `DATABASE_URL` — строка подключения к PostgreSQL
- `JWT_SECRET_KEY` — секрет подписи JWT (замените в продакшене!)
- `JWT_ALGORITHM` — алгоритм (по умолчанию `HS256`)
- `ACCESS_TOKEN_EXPIRES_DAYS` — срок жизни токена в днях (по умолчанию 30)

Пример для локального PostgreSQL:

```bash
export DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/lifebalance"
```

## Применение миграций БД

Из каталога `backend/` выполните:

```bash
alembic upgrade head
```

Ожидаемый результат — создание таблицы `users` с колонками: `id`, `email`, `password_hash`, `language_preference`, `created_at`, `updated_at` и типа перечисления `language_preference_enum` со значениями `ru`, `en`.

### Подробная проверка в PostgreSQL через psql

Подключитесь к базе и проверьте объекты (ожидается, что PostgreSQL и база из `DATABASE_URL` уже работают — этот раздел только про проверку результата):

```bash
psql "postgresql://postgres:postgres@localhost:5432/lifebalance"
```

Внутри psql выполните:

```sql
-- Список таблиц, должна быть public.users
\dt

-- Описание таблицы users: типы, default, not null, уникальность email
\d+ users

-- Значения enum language_preference_enum — должны быть ru, en
SELECT e.enumlabel
FROM pg_enum e
JOIN pg_type t ON t.oid = e.enumtypid
WHERE t.typname = 'language_preference_enum';

-- Проверка уникальности email (наличие ограничения/индекса)
SELECT conname, contype
FROM pg_constraint
WHERE conrelid = 'users'::regclass;
```

Ожидаемые моменты:
- `id` — uuid, `PRIMARY KEY`
- `email` — `character varying(320)`, `NOT NULL`, `UNIQUE`
- `password_hash` — `character varying(255)`, `NOT NULL`
- `language_preference` — `language_preference_enum`, `NOT NULL`, `DEFAULT 'en'`
- `created_at`, `updated_at` — `timestamp with time zone`, `DEFAULT now()`

### Если используете Docker Compose

1) Запустите сервисы:

```bash
cd backend
docker compose up -d
```

По умолчанию сервис `app` помечен профилем `api` и не стартует. Так удобнее для локальной разработки, когда API вы запускаете через локальный Uvicorn, а Postgres — в контейнере.

Чтобы запустить только Postgres: команда выше уже достаточно (стартует только `postgres`).

Чтобы запустить API в контейнере при необходимости:

```bash
docker compose --profile api up -d app
```

Чтобы запустить фронтенд (Vite dev server в контейнере, профиль `web`):

```bash
docker compose --profile web up -d frontend
```

После запуска фронт доступен на `http://localhost:5173`.

2) Примените миграции внутри контейнера приложения (если API запускаете в контейнере):

```bash
docker compose exec app bash -lc 'alembic upgrade head'
```

3) Проверьте схему в контейнере PostgreSQL:

```bash
docker compose exec -e PGPASSWORD=$POSTGRES_PASSWORD postgres \
  psql -U $POSTGRES_USER -d $POSTGRES_DB -c '\dt'
docker compose exec -e PGPASSWORD=$POSTGRES_PASSWORD postgres \
  psql -U $POSTGRES_USER -d $POSTGRES_DB -c '\d+ users'
docker compose exec -e PGPASSWORD=$POSTGRES_PASSWORD postgres \
  psql -U $POSTGRES_USER -d $POSTGRES_DB \
  -c "SELECT e.enumlabel FROM pg_enum e JOIN pg_type t ON t.oid = e.enumtypid WHERE t.typname = 'language_preference_enum';"
```

Подсказки по профилям Compose
- Сервис `app` помечен профилем `api` в `backend/docker-compose.yml`.
- Альтернатива: то же дублируется в `backend/docker-compose.override.yml` для удобной локальной конфигурации.
- Проверить список сервисов: `docker compose config --services`
- Запустить только Postgres: `docker compose up -d postgres`
- Запустить API по профилю: `docker compose --profile api up -d app`
- Остановить API: `docker compose stop app`
- Запустить фронтенд по профилю: `docker compose --profile web up -d frontend`
- Остановить фронтенд: `docker compose stop frontend`

## Запуск приложения

```bash
uvicorn app.main:app --reload
```

Сервис будет доступен по адресу `http://127.0.0.1:8000`.

## Запуск фронтенда (React)

Вариант 1 — локально:

```bash
cd frontend
npm install
npm run dev
```

Фронтенд откроется на `http://localhost:5173`. Для смены backend-URL можно задать `VITE_API_BASE_URL` (например, через `.env.local`).

Вариант 2 — через Docker Compose (см. профиль `web` выше).

### Когда перезапускать Uvicorn

В режиме разработки `--reload` сам перезапускает воркер при изменении .py файлов. Ручной рестарт нужен, если:
- Меняли переменные окружения/.env (`DATABASE_URL`, `JWT_SECRET_KEY`, `ACCESS_TOKEN_EXPIRES_DAYS`). Настройки кэшируются, без рестарта новые значения не подтянутся.
- Устанавливали/обновляли зависимости (`pip install`) или меняли версию Python.
- Меняли параметры запуска (порт/host), middleware/импорты, и это не попало под авто‑reload.
- Процесс «залип» или оставил занятым порт.

Когда не нужен рестарт:
- Правки кода .py — `--reload` перезапустит воркер автоматически.
- Применение миграций БД — сервер можно не трогать.

Как быстро перезапустить:
- Локально (в текущем терминале):
  - Остановить Ctrl+C и снова: `uvicorn app.main:app --reload`
- В фоне (устойчиво к закрытию терминала):
  - `nohup uvicorn app.main:app --reload > .uvicorn.log 2>&1 & disown`
  - Остановить: `pkill -f "uvicorn.*app.main:app"`
- Через Docker Compose (если API в контейнере):
  - `docker compose restart app`
  - или пересоздать: `docker compose --profile api up -d app --force-recreate`

## Быстрые проверки через curl

1) Регистрация пользователя

```bash
curl -sS -X POST http://127.0.0.1:8000/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"email":"user2@example.com","password":"secret12"}' | jq
```

Ожидается HTTP 201 и JSON с полями: `id`, `email`, `language_preference` (по умолчанию `en`), `created_at`.

2) Логин и получение токена

```bash
TOKEN=$(curl -sS -X POST http://127.0.0.1:8000/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"user2@example.com","password":"secret12"}' | jq -r .access_token)
echo "$TOKEN"
```

Ожидается HTTP 200 и поле `access_token`.

3) Текущий пользователь (Authorization: Bearer)

```bash
curl -sS http://127.0.0.1:8000/auth/me \
  -H "Authorization: Bearer $TOKEN" | jq
```

Ожидается HTTP 200 и JSON с данными пользователя.

4) Негативные сценарии

- Повторная регистрация того же `email` → HTTP 400, `{"detail": "Email already registered"}`
- Неверный пароль при логине → HTTP 401, `{"detail": "Invalid credentials"}`
- Без заголовка Authorization → HTTP 401, `{"detail": "Missing Authorization header"}`

## Скрипт демонстрации API

Для быстрого прогона есть `backend/scripts/demo_auth.sh`:

```bash
cd backend
./scripts/demo_auth.sh
```

Переменные окружения:
- `BASE_URL` (по умолчанию `http://127.0.0.1:8000`)
- `EMAIL` (случайный email по умолчанию)
- `PASS` (по умолчанию `secret12`)

Скрипт выводит JSON через `jq`, а при его отсутствии использует `python3 -m json.tool`.

## Прогон тестов

```bash
pytest -q
```

Ожидается: `8 passed, 0 warnings`.

Тесты находятся в `backend/tests/` и автоматически подготавливают схему БД для запуска.
Добавлены как unit-тесты роутов, так и интеграционный `test_auth_integration.py` (полный цикл register → login → me).

## Быстрый старт (Makefile)

Для удобства добавлен `Makefile` с типовыми командами (запускать из корня репозитория):

```bash
make help          # список доступных целей
make db-up         # поднять PostgreSQL в Docker
make migrate       # применить миграции Alembic
make api-run       # запустить API локально (uvicorn, reload)
make api-up        # запустить API в Docker (profile=api)
make fe-dev        # запустить фронтенд локально (Vite)
make fe-build      # собрать фронтенд
make fe-up         # запустить фронтенд в Docker (profile=web)
make demo          # demo: register -> login -> me (через curl)
make test          # прогон тестов backend
```

Переменные по умолчанию для `api-run`: `API_HOST=127.0.0.1`, `API_PORT=8000`. Можно переопределять: `make api-run API_PORT=8001`.

## Примечания по безопасности

- В продакшене обязательно задайте сильный `JWT_SECRET_KEY` и ограничьте CORS на нужные домены (см. `backend/app/main.py`).
- Токен живёт 30 дней (можно изменить через `ACCESS_TOKEN_EXPIRES_DAYS`).

## Где искать реализацию

- Security и JWT: `backend/app/core/security.py`
- Репозиторий: `backend/app/repositories/user_repository.py`
- Сервис: `backend/app/services/auth_service.py`
- Зависимости: `backend/app/api/deps.py`
- Роутер: `backend/app/api/auth.py`
- Приложение/CORS/роутинг: `backend/app/main.py`
