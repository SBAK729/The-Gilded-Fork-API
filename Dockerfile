# Use an official lightweight Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install OS dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc curl build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip first
RUN pip install --upgrade pip

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the default port (optional, Render auto-detects if bound properly)
EXPOSE 8000

# Command to run the app
# NOTE: This uses $PORT if set (e.g., by Render), else falls back to 8000
CMD ["sh", "-c", "uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
