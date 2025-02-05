FROM python:latest

COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD [".venv/bin/alembic", "upgrade", "head"]
# RUN alembic upgrade head