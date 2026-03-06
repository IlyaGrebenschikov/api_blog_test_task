# API Блога с Кешированием

REST API для блога с кешированием популярных постов в Redis.

## Архитектура

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   FastAPI   │ ────▶ │   Redis     │      │ PostgreSQL  │
│   (API)     │      │   (Cache)   │ ◀───▶│   (DB)      │
└─────────────┘      └─────────────┘      └─────────────┘
```

### Компоненты

| Компонент | Технология | Назначение |
|-----------|------------|------------|
| API | FastAPI | REST endpoints для CRUD операций |
| БД | PostgreSQL | Постоянное хранение постов |
| Кэш | Redis | Кеширование популярных постов |

### Почему такой подход к кешированию

1. **Ленивое кэширование** — посты кэшируются только после достижения порога популярности
2. **Настраиваемый порог** — значение `REDIS_HITS_THRESHOLD` задаётся в `.env` (по умолчанию: 10 просмотров)
3. **Настраиваемый TTL** — время жизни кэша задаётся в `.env` через `REDIS_POST_TTL` и `REDIS_HITS_TTL` (по умолчанию: 300 сек)
4. **Автоматическая инвалидация** — кэш обновляется при изменении/удалении поста
5. **Счётчик просмотров** — отдельный ключ для отслеживания популярности

### Структура ключей в Redis

| Ключ | Формат | TTL (из .env) |
|------|--------|---------------|
| Пост | `post:{id}` | `REDIS_POST_TTL` (300 сек) |
| Просмотры | `post:hits:{id}` | `REDIS_HITS_TTL` (300 сек) |

## Требования

- Docker и Docker Compose
- Python 3.14+ (для локальной разработки)

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/IlyaGrebenschikov/api_blog_test_task
cd api_blog_test_task
```

### 2. Настройка переменных окружения

Скопируйте файл `.env_example` в `.env` и при необходимости измените значения:

```bash
cp .env_example .env
```

**Переменные окружения:**

#### База данных (DB_)

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `DB_DRIVERNAME` | Драйвер БД | `postgresql+asyncpg` |
| `DB_HOST` | Хост PostgreSQL | — |
| `DB_PORT` | Порт PostgreSQL | `5432` |
| `DB_USERNAME` | Пользователь БД | — |
| `DB_PASSWORD` | Пароль БД | — |
| `DB_DATABASE` | Имя БД | — |

#### Сервер (UVICORN_SERVER_)

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `UVICORN_SERVER_HOST` | Хост сервера | `0.0.0.0` |
| `UVICORN_SERVER_PORT` | Порт сервера | `8080` |

#### Redis (REDIS_)

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `REDIS_HOST` | Хост Redis | `localhost` |
| `REDIS_PORT` | Порт Redis | `6379` |
| `REDIS_PASSWORD` | Пароль Redis | — |
| `REDIS_DB` | Номер БД Redis | `0` |
| `REDIS_POST_TTL` | TTL кэша постов (сек) | `300` |
| `REDIS_HITS_TTL` | TTL счётчика просмотров (сек) | `300` |
| `REDIS_HITS_THRESHOLD` | Порог популярности (просмотров) | `10` |

#### API V1 (V1_APP_)

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `V1_APP_TITLE` | Заголовок API | `FastAPI` |
| `V1_APP_VERSION` | Версия API | `0.1.0` |
| `V1_APP_DOCS_URL` | URL документации | `/docs` |
| `V1_APP_REDOC_URL` | URL ReDoc | `/redoc` |

#### CORS (V1_CORS_)

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `V1_CORS_METHODS` | Разрешённые методы | `*` |
| `V1_CORS_HEADERS` | Разрешённые заголовки | `*` |
| `V1_CORS_ORIGINS` | Разрешённые origins | `*` |

### 3. Запуск через Docker Compose

**Запуск всех сервисов (API, PostgreSQL, Redis):**

```bash
docker compose --profile api up -d
```

**Применение миграций БД:**

```bash
docker compose --profile migrations up migrations
```

**Проверка статуса:**

```bash
docker compose ps
```

### 4. Остановка сервисов

```bash
docker compose --profile api down
```

Для полной очистки (включая данные):

```bash
docker compose --profile api down -v
```

## API Endpoints

### POST /api/v1/posts
Создать новый пост

**Request:**
```json
{
  "title": "Заголовок",
  "content": "Содержимое"
}
```

**Response:** `201 Created`
```json
{
  "id": "uuid",
  "title": "Заголовок",
  "content": "Содержимое",
  "created_at": "2026-03-06T12:00:00",
  "updated_at": "2026-03-06T12:00:00"
}
```

---

### GET /api/v1/posts?post_id={id}
Получить пост по ID

**Response:** `200 OK`
```json
{
  "id": "uuid",
  "title": "Заголовок",
  "content": "Содержимое",
  "created_at": "2026-03-06T12:00:00",
  "updated_at": "2026-03-06T12:00:00"
}
```

**Response:** `404 Not Found` — пост не найден

---

### PATCH /api/v1/posts?post_id={id}
Обновить пост

**Request:**
```json
{
  "title": "Новый заголовок",
  "content": "Новое содержимое"
}
```

**Response:** `200 OK`

**Response:** `404 Not Found` — пост не найден

---

### DELETE /api/v1/posts?post_id={id}
Удалить пост

**Response:** `200 OK`

**Response:** `404 Not Found` — пост не найден

---

## Логика кеширования

### GET запрос поста

```
┌─────────────────────────────────────────────────────────┐
│  1. Проверка кэша (Redis)                               │
│     └─▶ Есть? ──▶ Вернуть из кэша + increment hits     │
│     └─▶ Нет? ──▶ Шаг 2                                  │
├─────────────────────────────────────────────────────────┤
│  2. Запрос из БД (PostgreSQL)                           │
├─────────────────────────────────────────────────────────┤
│  3. Увеличение счётчика просмотров                      │
├─────────────────────────────────────────────────────────┤
│  4. hits >= REDIS_HITS_THRESHOLD? ──▶ Да ──▶ Записать в кэш │
│                                     └─▶ Нет ──▶ Не кэшировать │
└─────────────────────────────────────────────────────────┘
```

### Обновление/Удаление поста

```
┌─────────────────────────────────────────────────────────┐
│  1. Операция в БД (UPDATE/DELETE)                       │
├─────────────────────────────────────────────────────────┤
│  2. Инвалидация кэша (DELETE из Redis)                  │
│     └─▶ post:{id}                                       │
│     └─▶ post:hits:{id}                                  │
└─────────────────────────────────────────────────────────┘
```

**Примечание:** Все параметры кеширования (порог просмотров, TTL) задаются в файле `.env` и могут быть изменены без модификации кода.

## Запуск тестов

**Запуск интеграционных тестов:**

```bash
# 1. Собрать приложение
docker compose build api

# 2. Поднять зависимости
docker compose --profile test up -d postgres redis

# 3. Применить миграции
docker compose --profile migrations up migrations

# 4. Запустить тесты
docker compose --profile test up test
```

**Остановка после тестов:**

```bash
docker compose --profile test down
```

## Структура проекта

```
src/
├── api_blog_test_task/
│   ├── application/          # Бизнес-логика
│   │   ├── services/         # Сервисы (PostsService)
│   │   ├── dto/              # Data Transfer Objects
│   │   ├── interfaces/       # Интерфейсы (репозитории, мапперы)
│   │   └── exceptions/       # Исключения
│   ├── domain/               # Доменные модели
│   │   └── entities/         # Сущности (Post)
│   ├── infrastructure/       # Инфраструктура
│   │   ├── database/         # PostgreSQL (репозитории, миграции)
│   │   ├── cache/            # Redis (репозитории)
│   │   └── di_providers/     # DI контейнеры (dishka)
│   ├── presentation/         # API layer
│   │   └── v1/
│   │       └── controllers/  # Контроллеры (posts.py)
│   └── core/                 # Общие настройки
tests/
├── conftest.py               # Фикстуры pytest
└── test_cache_api.py         # Интеграционные тесты кэша
```

## Технологии

| Категория | Технология |
|-----------|------------|
| Framework | FastAPI |
| БД | PostgreSQL + asyncpg |
| Кэш | Redis + redis-py |
| DI | dishka |
| Миграции | Alembic |
| Тесты | pytest + pytest-asyncio + httpx |
| Контейнеризация | Docker + Docker Compose |

## Обработка ошибок

| Код | Описание |
|-----|----------|
| `200 OK` | Успешный запрос |
| `201 Created` | Пост создан |
| `404 Not Found` | Пост не найден |
| `500 Internal Server Error` | Ошибка сервера |
