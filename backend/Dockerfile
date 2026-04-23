FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y libpq-dev gcc
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
# Проверяем, что порт совпадает с логами
ENV PORT=8080
CMD ["python", "app.py"]
