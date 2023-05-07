ARG PYTHON_VERSION=3.10-slim-buster

ARG DEBIAN_FRONTEND=noninteractive

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code

WORKDIR /code

#install the linux packages, since these are the dependencies of some python packages
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/* !

COPY requirements.txt /tmp/requirements.txt

RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/

COPY . /code

# RUN python manage.py collectstatic -- noinput

CMD ["gunicorn", "--workers", "2", "project.wsgi"]