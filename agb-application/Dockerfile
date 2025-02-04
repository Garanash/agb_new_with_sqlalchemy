FROM python:3.13-slim

# Установка зависимостей
COPY requirements.txt .
RUN pip install -r requirements.txt

# Установка утилит для проверки готовности PostgreSQL
RUN apt-get update && apt-get install -y postgresql-client

# Копирование приложения
COPY . .

# Добавьте эту команду для проверки готовности PostgreSQL
COPY docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]