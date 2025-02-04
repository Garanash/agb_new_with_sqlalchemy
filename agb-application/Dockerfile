FROM python:3.13-slim

# Установка зависимостей
COPY requirements.txt .
RUN pip install -r requirements.txt

# Копирование приложения
COPY . .

# Создание директории для миграций
RUN mkdir -p /agb-application/alembic
WORKDIR /agb-application

# Добавьте эту команду для проверки готовности PostgreSQL
COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]