# Warehouse API

## Описание
API для работы со складом. 
Позволяет добавлять, удалять и редактировать товары на складе, 
получать список всех товаров и информацию о конкретном товаре.
Создавать заказ, получать список всех заказов, информацию о конкретном заказе,
обновлять статус заказа.

## Технологии
- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Poetry
- Docker

## Установка и запуск
1. Склонировать репозиторий командой: 
    "git clone https://github.com/MD-shka/warehouse.git"
2. Перейти в папку проекта: "cd warehouse"
3. Запустить командой: "docker-compose up --build"

## Документация
1. Документация Swagger: http://localhost:8000/docs
2. Документация Redoc: http://localhost:8000/redoc

## Тестирование
 Запустить тесты командой: "docker-compose exec web pytest"
