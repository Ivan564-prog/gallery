FROM python:3.12-slim 

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN addgroup --system gunicorn && \
    useradd -g gunicorn -p '' -m --home /home/gunicorn gunicorn && \
    apt-get update && apt-get install -y cron

COPY ./backend/requirements.txt /app/requirements.txt
COPY ./backend/packages /app/packages

RUN pip install --no-cache-dir -r /app/requirements.txt 

WORKDIR /app

COPY --chown=gunicorn:gunicorn ./backend /app

# RUN echo "* * * * * gunicorn cd /app && /usr/local/bin/python3 /app/manage.py example_1        >> /app/logs/cron.log 2>&1 " >> /etc/crontab
# RUN echo "* * * * * gunicorn cd /app && /usr/local/bin/python3 /app/manage.py test             >> /app/logs/cron.log 2>&1 " >> /etc/crontab

CMD [ "sh", "entrypoint.sh" ]
