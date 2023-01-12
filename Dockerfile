FROM python:3.9-alpine3.13
LABEL maintainer="larisa.elena.paliciuc@gmail.com"

# displays output on directly terminal
ENV PYTHONUNBUFFERED 1

# copy the app and req to the image container
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

#currently overwritten by docker-compose with TRUE
ARG DEV=false
# uses venv, upgrades pip, installs the req, deletes files under tmp and creates the django user
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/py/bin:$PATH"

USER django-user