FROM python:3.11

RUN mkdir -p /home/app

ENV PYTHONUNBUFFERED 1

ENV PYTHONDONTWRITEBYTECODE 1

# create the appropriate directories
ENV HOME=/home/app

ENV APP_HOME=/home/app/

WORKDIR ${APP_HOME}

COPY ./requirements.txt ${APP_HOME}

RUN pip install -r requirements.txt

# RUN python manage.py collectstatic --noinput

COPY . ${APP_HOME}