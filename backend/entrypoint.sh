printenv |grep ^PG_USERNAME= >> /etc/environment
printenv |grep ^PG_PASSWORD= >> /etc/environment
printenv |grep ^PG_DATABASE= >> /etc/environment
printenv |grep ^PG_HOST= >> /etc/environment
printenv |grep ^HOST= >> /etc/environment
cron -f&
su -c 'python3 manage.py collectstatic --noinput && python3 manage.py migrate && gunicorn -b 0.0.0.0:8000 system.wsgi' gunicorn