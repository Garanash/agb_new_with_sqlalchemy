FROM python:latest

COPY . /agb-application
WORKDIR /agb-application/

RUN pip install --no-cache-dir -r requirements.txt

# RUN alembic upgrade head