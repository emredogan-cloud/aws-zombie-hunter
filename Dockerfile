# Multi-stage build for AWS Zombie Hunter
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# VENV (Sanal Ortam) oluştur ve aktif et
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy and install Python dependencies
COPY requirements.txt .
# --user yerine doğrudan VENV içine kuruyoruz
RUN pip install --no-cache-dir -r requirements.txt


# Final stage
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies (ca-certificates for AWS HTTPS calls)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy VENV from builder
COPY --from=builder /opt/venv /opt/venv

# Set Python config & VENV Path
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Create non-root user for security
RUN useradd -m -u 1000 zombie && chown -R zombie:zombie /app
USER zombie

# Copy project files (Dosyaların sahipliğini baştan zombie'ye veriyoruz)
COPY --chown=zombie:zombie . .

# Volume for AWS credentials
VOLUME ["/home/zombie/.aws"]

# Health check - verify Python environment
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import boto3; print('AWS SDK ready')" || exit 1

# Default command
ENTRYPOINT ["python", "main.py"]
CMD []