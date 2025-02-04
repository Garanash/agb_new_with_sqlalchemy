#!/bin/bash

# Функция для проверки готовности PostgreSQL
wait_for_postgres() {
    while ! pg_isready -h postgres -p 5432; do
        echo "PostgreSQL не готов, ожидание..."
        sleep 2
    done
    echo "PostgreSQL готов"
}

# Ждем готовности PostgreSQL
wait_for_postgres

# Выполняем миграции
echo "Выполнение миграций..."
#alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

# Запускаем приложение
exec "$@"