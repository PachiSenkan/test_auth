# Тестовое задание Кочев Д.А.

## Запуск
1. Клонировать репозиторий
  ```
  git clone https://github.com/PachiSenkan/test_auth.git
  ```
3. Перейти в папку test_auth
4. Создать виртуальное окружение
**Windows:**
  ```
  python -m venv venv
  /venv/Scripts/activate
  ```
**Linux:**
  ```
  python3 -m venv venv
  source venv/bin/sctivate
  ```
5. Установить зависимости
**Windows:**
  ```
  python -m pip -r requirements.txt
  ```
**Linux:**
  ```
  python3 -m pip -r requirements.txt
  ```
6. Запустить сервер
  ```
  uvicorn app.main:app --reload
  ```
После запуска эндпоинты доступны по адресу `127.0.0.1:8000/api/v1/` или через Swagger `127.0.0.1:8000/docs/`
