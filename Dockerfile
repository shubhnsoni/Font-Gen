FROM python:3.11-slim

# Install dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY backend.py ./

# Expose API port
EXPOSE 5050

CMD ["python", "backend.py"]
