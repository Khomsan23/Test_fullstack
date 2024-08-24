# Dockerfile ในโฟลเดอร์ server
FROM python:3.9-slim

WORKDIR /app

# คัดลอกไฟล์ requirements.txt
COPY requirements.txt /app/requirements.txt

# ติดตั้ง dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# คัดลอกไฟล์โปรเจกต์
COPY . /app

# รันคำสั่งเริ่มต้น
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
