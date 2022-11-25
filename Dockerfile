FROM python:3.9-alpine3.13
LABEL maintainer="SAI"

ENV PYTHONBUFFERED 1

COPY ./req.txt /tmp/req.txt
COPY ./app /app
WORKDIR /app
EXPOSE 5000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/req.txt && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        flask-user

ENV PATH="/py/bin:$PATH"

USER flask-user