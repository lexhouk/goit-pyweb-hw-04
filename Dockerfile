FROM python:3.10.14-alpine3.20

WORKDIR /app
COPY . .

VOLUME /app/www/storage
EXPOSE 3000

CMD ["python", "main.py"]
