FROM python:3.11

RUN mkdir -p /home/app

ENV PYTHONUNBUFFERED 1

ENV PYTHONDONTWRITEBYTECODE 1

# create the appropriate directories
ENV HOME=/home/app

ENV APP_HOME=/home/app

WORKDIR ${APP_HOME}

COPY ./requirements.txt ${APP_HOME}

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . ${APP_HOME}

RUN python manage.py makemigrations && \
    python manage.py migrate && \
    python manage.py collectstatic --noinput && \
    celery -A eduprene worker -l info --detach

EXPOSE 8001

CMD ["gunicorn" , "eduprene.wsgi:application", "--bind", "0.0.0.0:8001"]