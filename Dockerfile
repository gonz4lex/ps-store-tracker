# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy pyproject.toml and lock first for caching
COPY pyproject.toml uv.lock ./

# Install uv and dependencies
RUN pip install --upgrade pip
RUN pip install uv
RUN uv install

# Copy the rest of the code
COPY src/ ./src/
COPY scripts/ ./scripts/
COPY data/ ./data/

# Set environment variables for Streamlit
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLECORS=false

# Expose Streamlit port
EXPOSE 8501

# Command to run Streamlit app
CMD ["streamlit", "run", "src/ps_store_tracker/app.py"]
