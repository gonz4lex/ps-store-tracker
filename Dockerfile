# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies and create non-root user
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/* && \
    useradd -m -u 1000 appuser

# Copy uv binary from official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files for better cache efficiency
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy application code
COPY --chown=appuser:appuser src/ ./src/
COPY --chown=appuser:appuser scripts/ ./scripts/
COPY --chown=appuser:appuser data/ ./data/

# Switch to non-root user
USER appuser

# Set environment variables for Streamlit
ENV STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_ENABLECORS=false \
    PYTHONUNBUFFERED=1

# Expose Streamlit port
EXPOSE 8501

# Command to run Streamlit app
CMD ["uv", "run", "streamlit", "run", "src/ps_store_tracker/app.py"]