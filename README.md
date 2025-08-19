# TsApi – Система управления доступом и товарами

## 📌 Описание
Проект реализует **RBAC (Role-Based Access Control)** для управления доступом пользователей к товарам.  
Все пользователи имеют роли, а роли привязаны к набору прав (`view`, `create`, `update`, `delete`).  
Аутентификация выполняется через **JWT**, который сохраняется в `cookie`.

---

## 🚀 Быстрый старт

### Предварительные требования
*   Python 3.8+
*   Django 3.2+
*   Django REST Framework

### Установка и запуск

1.  **Установите зависимости:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Примените миграции:**
    ```bash
    python manage.py migrate
    ```

3.  **Запустите сервер:**
    ```bash
    python manage.py runserver
    ```

4.  **Сервер будет доступен по адресу:** `http://127.0.0.1:8000/`

---

## 👥 Пользователи, роли и права

### Доступные роли
*   **`admin`** — имеет все права (`view`, `create`, `update`, `delete`)
*   **`manager`** — может просматривать и редактировать товары
*   **`guest`** — может только просматривать товары

### Права доступа
*   `view` — просмотр товаров
*   `create` — добавление товаров
*   `update` — изменение товаров  
*   `delete` — удаление товаров

---

## 🔐 Аутентификация

Используется **JWT (JSON Web Token)**. При успешном входе токен сохраняется в HTTP-only cookie.

---

## 📡 API Эндпоинты

### 🔐 Аутентификация и пользователи (`/api/auth/`)

*   **`POST /api/auth/register/`** — Регистрация нового пользователя
    ```json
    {
      "first_name": "Ivan",
      "last_name": "Ivanov",
      "email": "ivan@example.com",
      "password": "securepassword123",
      "role": "guest" // Опционально. Если не указать, будет назначена роль "guest"
    }
    ```

*   **`POST /api/auth/login/`** — Вход в систему
    ```json
    {
      "email": "ivan@example.com",
      "password": "securepassword123"
    }
    ```

*   **`POST /api/auth/logout/`** — Выход из системы (удаляет JWT cookie)

*   **`POST /api/auth/update/`** — Обновление данных профиля (требуется авторизация)

*   **`DELETE /api/auth/delete/`** — Удаление аккаунта (требуется авторизация)

*   **`GET /api/auth/roles/permissions/`** — Список ролей и прав (только для `admin`)

*   **`POST /api/auth/roles/permissions/`** — Обновление прав для роли (только для `admin`)
    ```json
    {
      "role": "manager",
      "permissions": ["view", "update"]
    }
    ```

### 📦 Товары (`/api/goods/`)

*   **`GET /api/goods/products/`** — Получить список всех товаров
*   **`GET /api/goods/products/<id>/`** — Получить данные конкретного товара
*   **`POST /api/goods/products/`** — Создать новый товар (требуется право `create`)
    ```json
    {
      "name": "Ноутбук",
      "price": 60000,
      "description": "Игровой ноутбук"
    }
    ```
*   **`PUT /api/goods/products/<id>/`** — Обновить данные товара (требуется право `update`)
*   **`DELETE /api/goods/products/<id>/`** — Удалить товар (требуется право `delete`)

---
