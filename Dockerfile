FROM python:3.10-slim


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


RUN apt-get update && \
    apt-get install -y netcat gcc postgresql-client && \
    apt-get clean


WORKDIR /app


COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app/

CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
