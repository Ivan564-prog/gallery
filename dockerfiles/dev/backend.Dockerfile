FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

RUN addgroup --system gunicorn && \
    useradd -g gunicorn -p '' -m --home /home/gunicorn gunicorn

COPY ./backend/requirements.txt /app/requirements.txt
COPY ./backend/packages /app/packages

WORKDIR /app

RUN pip install -r requirements.txt

COPY --chown=gunicorn:gunicorn ./backend /app

USER gunicorn

CMD ["sh", "-c", \
                "python3 manage.py collectstatic --noinput \
                # && python3 manage.py makemigrations \
                && python3 manage.py migrate \
                && gunicorn --reload -b 0.0.0.0:8000 system.wsgi"]
