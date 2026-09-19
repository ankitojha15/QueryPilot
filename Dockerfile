# Small image for QueryPilot API + UI.
FROM python:3.12-slim

# Run in /app folder.
WORKDIR /app

# Install deps first for fast rebuild.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all code.
COPY . .

# Render gives PORT, run on it.
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port $PORT"]
