FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies required by WeasyPrint and uv
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libxml2-dev \
    libxslt1-dev \
    libjpeg-dev \
    zlib1g-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Copy project files
COPY . /app

# Install Python dependencies using uv
RUN uv pip install --no-cache --system -r requirements.lock

# Expose port for FastAPI
EXPOSE 8080

# Start FastAPI app
CMD ["uvicorn", "parts2sales_llm_hub.main:app", "--host", "0.0.0.0", "--port", "8080"]
