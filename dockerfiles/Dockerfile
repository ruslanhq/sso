FROM nginx/unit:1.23.0-python3.9

WORKDIR /app
COPY requirements.txt /app/

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install -r requirements.txt
COPY ./dockerfiles/config.json /docker-entrypoint.d/
COPY . /app
RUN python manage.py collectstatic

EXPOSE 8001
