
Сервис доступен через веб-интерфейс и REST API.

---

## ⚙️ Технологии

### Backend

* **Python** — язык.
* **FastAPI** — REST API.
* **SQLAlchemy + Alembic** — ORM + миграции.
* **PostgreSQL** — основная база данных.
* **Redis** — кеш и хранение сессий.
* **pytest** — тестирование.
* **Docker + docker-compose** — контейнеризация.
* **CI/CD** — автоматические тесты, сборка образов, деплой.
* **AWS/GCP** — инфраструктура (API, база, Redis).

### Frontend

* **React (TypeScript)** — веб-интерфейс.
* **React Router** — роутинг.
* **Axios/Fetch** — работа с API.
* **Material UI (MUI)** или **Tailwind** — UI-компоненты.
* **JWT Auth** — авторизация через токен.
* Сборка и деплой через **Docker** и CI/CD в AWS Amplify / GCP Hosting / Netlify.

---

## 🗄️ Схема данных (Backend)

**User** → **Habit** → **HabitLog** (как раньше описывал).

---

## 🔑 Основные функции

### Backend API

* Регистрация / логин пользователей (JWT).
* CRUD для привычек.
* Логирование выполнения привычек.
* Подсчёт streak и выдача статистики.

### Frontend (React)

* **Аутентификация**: регистрация, вход, выход.
* **Dashboard**: список привычек, текущий streak.
* **Форма добавления привычки** (название, описание, периодичность).
* **Отметка выполнения** привычки за день.
* **График/таблица streak** (например, с помощью recharts).

---

## 🐳 Docker

* `api` (FastAPI)
* `frontend` (React)
* `db` (Postgres)
* `redis`
* `nginx` (reverse proxy для фронта и апи)

---

## 🔁 CI/CD

* Линтеры и тесты при каждом пуше.
* Сборка Docker-образов (frontend + backend).
* Деплой:

  * **Backend** → AWS ECS / GCP Cloud Run.
  * **Frontend** → AWS Amplify / GCP Firebase Hosting / Netlify.
  * **DB + Redis** → RDS/Cloud SQL + ElastiCache/Memorystore.
