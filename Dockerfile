FROM python:3.12.3-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000

# Команда для запуска. Для тестирования я запускал вручную из виртуального окружения.
CMD ["python", "main.py"]
