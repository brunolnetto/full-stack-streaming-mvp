FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/main.py ./main.py

CMD ["uv", "main:app", "--host", "0.0.0.0", "--port", "8000"] 