# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt pyproject.toml ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY main.py web_app.py ./

# Create non-root user for security
RUN groupadd -r nexus && useradd -r -g nexus nexus \
    && chown -R nexus:nexus /app

# Create logs directory
RUN mkdir -p /app/logs && chown -R nexus:nexus /app/logs

# Switch to non-root user
USER nexus

# Expose port for web interface
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Default command (can be overridden)
CMD ["python", "main.py"]

# Labels for metadata
LABEL maintainer="Nexus Team <support@nexus-ai.com>" \
      version="1.0.0" \
      description="Nexus AI Assistant - Intelligent AI assistant for natural language processing" \
      org.opencontainers.image.source="https://github.com/yourusername/nexus"
