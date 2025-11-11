FROM python:3.11.9-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY requirements.txt .
COPY ./ddsc_web ./ddsc_web

RUN pip install --upgrade pip setuptools
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /usr/src/app/ddsc_web

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "ddsc_web.wsgi:application"]
