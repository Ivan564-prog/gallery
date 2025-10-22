FROM python:3.12-slim 

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN addgroup --system gunicorn && \
    useradd -g gunicorn -p '' -m --home /home/gunicorn gunicorn && \
    apt-get update

COPY ./backend/requirements.txt /app/requirements.txt
COPY ./backend/packages /app/packages

RUN pip install --no-cache-dir -r /app/requirements.txt 

WORKDIR /app

COPY --chown=gunicorn:gunicorn ./backend /app

CMD ["sh", "-c", \
                "python3 manage.py collectstatic --noinput \
                && python3 manage.py migrate \
                # && gunicorn -b 0.0.0.0:8000 system.wsgi
                && granian --host 0.0.0.0 --port 8000 --interface wsgi system.wsgi:application"]

# RUN echo "* * * * * gunicorn cd /app && /usr/local/bin/python3 /app/manage.py example_1        >> /app/logs/cron.log 2>&1 " >> /etc/crontab
# RUN echo "* * * * * gunicorn cd /app && /usr/local/bin/python3 /app/manage.py test             >> /app/logs/cron.log 2>&1 " >> /etc/crontab

# CMD [ "sh", "entrypoint.sh" ]
# CMD [ "sh", "entrypoint.sh" ]
