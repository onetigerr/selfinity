## Структура Backend проекта

```
backend/
├── alembic/                    # миграции БД
│   ├── versions/
│   └── env.py
├── app/
│   ├── api/                    # API layer (Presentation)
│   │   ├── deps.py            # FastAPI dependencies
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py        # /api/v1/auth/*
│   │   │   ├── sessions.py    # /api/v1/sessions/*
│   │   │   ├── problems.py    # /api/v1/problems/*
│   │   │   ├── solutions.py   # /api/v1/solutions/*
│   │   │   └── users.py       # /api/v1/users/*
│   │   └── router.py
│   ├── core/                   # Configuration
│   │   ├── config.py          # pydantic settings
│   │   ├── security.py        # JWT, password hashing
│   │   └── database.py        # SQLAlchemy session
│   ├── models/                 # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── life_area.py
│   │   ├── assessment.py
│   │   ├── problem.py
│   │   └── solution.py
│   ├── schemas/                # Pydantic DTOs
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── session.py
│   │   ├── problem.py
│   │   └── solution.py
│   ├── services/               # Business Logic layer
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   ├── session_service.py
│   │   ├── problem_service.py
│   │   └── solution_service.py
│   ├── repositories/           # Data Access layer (DAOs)
│   │   ├── __init__.py
│   │   ├── base.py            # Base repository class
│   │   ├── user_repository.py
│   │   ├── session_repository.py
│   │   ├── problem_repository.py
│   │   └── solution_repository.py
│   ├── exceptions.py           # Custom exceptions
│   └── main.py                 # FastAPI app initialization
├── tests/
│   ├── unit/
│   │   ├── test_services/
│   │   └── test_repositories/
│   ├── integration/
│   │   └── test_api/
│   └── conftest.py            # pytest fixtures
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── pytest.ini
└── alembic.ini
```

***

## Структура Frontend проекта

```
frontend/
├── src/
│   ├── core/
│   │   ├── config/
│   │   │   └── constants.ts
│   │   ├── api/
│   │   │   ├── client.ts       # axios instance + interceptors
│   │   │   └── endpoints.ts
│   │   ├── i18n/
│   │   │   ├── i18n.ts         # i18next config
│   │   │   ├── locales/
│   │   │   │   ├── en.json
│   │   │   │   └── ru.json
│   │   ├── hooks/              # Global hooks
│   │   │   └── useAuth.ts
│   │   ├── context/
│   │   │   └── AuthContext.tsx
│   │   ├── types/              # Global types
│   │   │   └── index.ts
│   │   └── utils/
│   │       └── storage.ts      # JWT token management
│   ├── layouts/
│   │   ├── MainLayout.tsx
│   │   ├── AuthLayout.tsx
│   │   └── components/
│   │       ├── Header.tsx
│   │       └── Sidebar.tsx
│   ├── features/
│   │   ├── auth/
│   │   │   ├── components/
│   │   │   │   ├── LoginForm.tsx
│   │   │   │   └── RegisterForm.tsx
│   │   │   ├── hooks/
│   │   │   │   ├── useLogin.ts
│   │   │   │   └── useRegister.ts
│   │   │   ├── types/
│   │   │   │   └── auth.types.ts
│   │   │   ├── views/
│   │   │   │   ├── LoginView.tsx
│   │   │   │   └── RegisterView.tsx
│   │   │   └── routes.tsx
│   │   ├── dashboard/
│   │   │   ├── components/
│   │   │   │   ├── LifeWheelChart.tsx
│   │   │   │   ├── SessionHistory.tsx
│   │   │   │   └── QuickStats.tsx
│   │   │   ├── hooks/
│   │   │   │   └── useDashboard.ts
│   │   │   ├── views/
│   │   │   │   └── DashboardView.tsx
│   │   │   └── routes.tsx
│   │   ├── assessment/
│   │   │   ├── components/
│   │   │   │   ├── ScoreSlider.tsx
│   │   │   │   ├── SessionForm.tsx
│   │   │   │   └── LifeAreaCard.tsx
│   │   │   ├── hooks/
│   │   │   │   ├── useCreateSession.ts
│   │   │   │   └── useUpdateScores.ts
│   │   │   ├── types/
│   │   │   │   └── assessment.types.ts
│   │   │   ├── views/
│   │   │   │   ├── NewAssessmentView.tsx
│   │   │   │   └── SessionDetailView.tsx
│   │   │   └── routes.tsx
│   │   ├── problems/
│   │   │   ├── components/
│   │   │   │   ├── ProblemList.tsx
│   │   │   │   ├── ProblemForm.tsx
│   │   │   │   ├── ProblemCard.tsx
│   │   │   │   ├── SolutionList.tsx
│   │   │   │   └── SolutionForm.tsx
│   │   │   ├── hooks/
│   │   │   │   ├── useProblems.ts
│   │   │   │   └── useSolutions.ts
│   │   │   ├── types/
│   │   │   │   └── problem.types.ts
│   │   │   ├── views/
│   │   │   │   ├── ProblemsView.tsx  # по конкретной сфере
│   │   │   │   └── AllProblemsView.tsx
│   │   │   └── routes.tsx
│   │   └── profile/
│   │       ├── components/
│   │       │   ├── LanguageSwitcher.tsx
│   │       │   └── ProfileForm.tsx
│   │       ├── hooks/
│   │       │   └── useProfile.ts
│   │       ├── views/
│   │       │   └── ProfileView.tsx
│   │       └── routes.tsx
│   ├── router.tsx              # Aggregated routing
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
├── public/
├── package.json
├── tsconfig.json
├── vite.config.ts
├── Dockerfile
└── .env.example
```

***

## Технологический стек - финальный список

### Backend
- Python 3.11+[6]
- FastAPI[6]
- SQLAlchemy 2.0 + Alembic[6]
- PostgreSQL 15+[6]
- Redis 7+[6]
- Pydantic v2 для валидации[2]
- python-jose для JWT[1]
- passlib для хеширования паролей[1]
- pytest + pytest-asyncio[6]
- Docker + docker-compose[6]

### Frontend
- React 18+[6]
- TypeScript 5+[6]
- Vite[3]
- React Router v6[6]
- Axios[6]
- Material UI v5 или Tailwind CSS v3[6]
- Chart.js + react-chartjs-2 (для Life Wheel)[8]
- react-i18next для локализации[3]
- React Hook Form для форм[3]
- Zustand или Context API для state management[3]

### Infrastructure
- Docker для контейнеризации[6]
- GitHub Actions для CI/CD[6]
- AWS (ECS, RDS, ElastiCache, S3) или GCP (Cloud Run, Cloud SQL, Memorystore)[6]

***

## Приоритеты для MVP

**Must have (первые 4-6 недель):**
1. Авторизация (email/password)[6]
2. Создание и завершение сессий оценки[5]
3. CRUD проблем и решений (лимит 8 на сферу)[5]
4. Базовая круговая диаграмма Life Wheel[5]
5. История сессий[5]
6. Локализация ru/en[6]

**Nice to have (следующие итерации):**
1. OAuth аутентификация[6]
2. Версионирование истории изменений[5]
3. Экспорт данных в PDF/CSV[5]
4. Валидация формулировок проблем/решений через LLM[5]
5. Интеграции с внешними сервисами[5]
6. Офлайн режим[5]