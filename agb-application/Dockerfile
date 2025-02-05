FROM python:latest

RUN echo "127.0.0.1 host.docker.internal" >> /etc/hosts

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["alembic", "upgrade", "head"]