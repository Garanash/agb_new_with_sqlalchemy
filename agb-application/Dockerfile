FROM python:latest

COPY . .
RUN python -m venv .venv
RUN source .venv/bin/activate
RUN pip install --no-cache-dir -r requirements.txt
CMD [".venv/bin/alembic", "upgrade", "head"]
# RUN alembic upgrade head