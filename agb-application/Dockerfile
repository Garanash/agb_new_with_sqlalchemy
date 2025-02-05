FROM python:latest

COPY . /agb-application
WORKDIR /agb-application/
RUN python3 -m venv .venv
RUN source .venv/bin/activate
RUN pip install --no-cache-dir -r requirements.txt

# RUN alembic upgrade head