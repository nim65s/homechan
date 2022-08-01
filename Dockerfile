FROM python:3.10-slim

EXPOSE 8000

WORKDIR /app

ENV PYTHONUNBUFFERED=1

CMD while ! nc -z postgres 5432; do sleep 1; done \
 && ./manage.py migrate \
 && ./manage.py collectstatic --no-input \
 && daphne \
    -b 0.0.0.0 \
    homechan.asgi:application

ADD . .

RUN --mount=type=cache,sharing=locked,target=/var/cache/apt \
    --mount=type=cache,sharing=locked,target=/var/lib/apt \
    --mount=type=cache,sharing=locked,target=/root/.cache \
    apt-get update -y && DEBIAN_FRONTEND=noninteractive apt-get install -qqy \
    gcc \
    git \
    libexpat1 \
    libpq-dev \
    netcat \
 && python -m pip install -U pip \
 && python -m pip install \
    psycopg2 \
 && python -m pip install . \
 && apt-get autoremove -qqy gcc
