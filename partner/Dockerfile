FROM python:3.9-slim


WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y python3-dev default-libmysqlclient-dev build-essential pkg-config && pip install -r requirements.txt

EXPOSE 5100

CMD ["python","app.py"]