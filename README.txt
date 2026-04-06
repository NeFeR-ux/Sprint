# FSTR Pereval API

API для добавления и управления информацией о горных перевалах.

## Установка и запуск

```bash
# Клонирование
git clone https://github.com/NeFeR-ux/mmorpg_board.git
cd mmorpg_board

# Установка зависимостей
pip install -r requirements.txt

# Создай файл .env с настройками БД

# Запуск
uvicorn app.main:app --reload