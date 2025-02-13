# 📌 CRM-система для малого бизнеса

## 📖 Описание
CRM-система предназначена для управления клиентами, сделками и задачами малого бизнеса. Она позволяет автоматизировать работу менеджеров, вести учет клиентов и сделок, а также анализировать бизнес-показатели.

## 🚀 Функциональность
- 📋 **Управление клиентами** (создание, редактирование, удаление, фильтрация)
- 🤝 **Работа со сделками** (статусы, менеджеры, стоимость, аналитика)
- 📅 **Задачи для сотрудников** (назначение, статусы, приоритеты)
- 🔐 **Аутентификация и роли** (JWT, доступ по ролям)
- 📊 **Аналитика** (доход, статистика по сделкам)
- 📩 **Уведомления** (Email)

---

## 🛠️ Стек технологий
- **Backend**: Django + DRF
- **Database**: PostgreSQL
- **Асинхронные задачи**: Celery + Redis
- **Документация API**: Swagger
- **Тестирование**: Pytest, Django Test Client

---

## 🏗️ Установка и настройка

### 🔧 1. Клонирование репозитория
```bash
git clone https://github.com/your-repo/crm-system.git
cd crm-system
```

### 📦 2. Создание виртуального окружения
```bash
python -m venv venv
source venv/bin/activate  # Для Windows: venv\Scripts\activate
```

### 📌 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 🛠️ 4. Настройка переменных окружения
Создайте `.env` файл и добавьте:
```ini
SECRET_KEY=
DEBUG=True
ALLOWED_HOSTS=''

PG_DATABASE=postgres
PG_USER=postgres
PG_PASSWORD='your_password'
DB_PORT=5432
DB_HOST=localhost

EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=

REDIS_URL=redis://localhost:6379/0

CELERY_TASK_TRACK_STARTED=True

CELERY_TASK_TIME_LIMIT=1800

ACCEPT_CONTENT=json
RESULT_SERIALIZER=json
TASK_SERIALIZER=json

TIMEZONE=
```

### 🚀 5. Применение миграций
```bash
python manage.py migrate
python manage.py createsuperuser  # Создание администратора
```

### ▶️ 6. Запуск сервера
```bash
python manage.py runserver
```

---

## 🔗 API Эндпоинты

### 🔐 Аутентификация
- `POST /api/auth/jwt/create/` – Создание токена
- `POST /api/auth/jwt/refresh/` – Обновление токена
- `POST /api/auth/jwt/verify/` – Проверка токена

### 👤 Пользователь
- `POST /api/auth/activate/` – Активация учетной записи
- `POST /api/auth/registration/` – Регистрация пользователя
- `GET /api/auth/user_list/` – Получение списка пользователей
- `GET /api/auth/user_search/` – Поиск пользователей
- `PATCH /api/auth/user_update/` – Частичное обновление пользователя
- `PUT /api/auth/user_update/` – Полное обновление пользователя

### 🔐 Пароль
- `POST /api/password/change_password/` – Смена пароля
- `POST /api/password/reset_password/` – Запрос на сброс пароля
- `POST /api/password/reset_password_confirm/` – Подтверждение сброса пароля

### 👥 Клиенты
- `POST /api/clients/` – Регистрация нового клиента
- `GET /api/clients/` – Список клиентов
- `GET /api/clients/search/` – Поиск клиента
- `PATCH /api/clients/{id}/` – Частичное обновление клиента
- `PUT /api/clients/{id}/` – Полное обновление клиента
- `DELETE /api/clients/{id}/` – Удаление клиента
- `GET /api/clients/{id}/` – Просмотр клиента

### 🤝 Сделки
- `POST /api/deals/` – Создание сделки
- `GET /api/deals/` – Список сделок
- `PATCH /api/deals/{id}/` – Обновление сделки
- `DELETE /api/deals/{id}/` – Удаление сделки

### 📄 Задачи
- `POST /api/tasks/` – Создание задачи
- `GET /api/tasks/` – Список задач
- `PATCH /api/tasks/{id}/` – Частичное обновление задачи
- `PUT /api/tasks/{id}/` – Полное обновление задачи
- `DELETE /api/tasks/{id}/` – Удаление задачи


---

## ✅ Тестирование * In Develompent
```bash
pytest
```

---

## 📦 Деплой * In Develompent
### 📌 1. Запуск через Docker
```bash
docker-compose up --build
```

### 📌 2. Запуск Celery
```bash
celery -A config worker --loglevel=info
```

### 📌 3. Запуск Flower (Мониторинг Celery) * In Develompent
```bash
celery -A crm_system flower
```

---

## ✨ Авторы
**Разработчик**: [ibrohim-Fazliddinov]

