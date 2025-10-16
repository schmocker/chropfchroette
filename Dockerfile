FROM python:3.12-slim

# Install system dependencies (optional: for building some wheels)
RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential
RUN rm -rf /var/lib/apt/lists/*

# Install uv (fast Python package manager)
RUN pip install --no-cache-dir uv

# Set work directory
WORKDIR /app

# Copy dependency files first for better caching
# If you have pyproject.toml and optionally uv.lock, copy them
COPY pyproject.toml uv.lock* ./

# Install dependencies with uv
# - Prefer using the lock file if present for reproducibility
RUN if [ -f uv.lock ]; then \
      uv sync --frozen --no-dev; \
    else \
      uv sync --no-dev; \
    fi

# Copy the application source
COPY . .

# Expose the port (Flask default is 5000; we’ll run on 8000)
EXPOSE 8000

# Environment variables
# - Prevent Python from writing .pyc files
# - Ensure output is unbuffered
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the default command:
# Use uv run to execute the module, pointing to app/app.py where the Flask instance is "app"
# Running with flask's built-in server for simplicity; replace with a production server if needed
CMD ["uv", "run", "python", "-m", "flask", "--app=app/app.py:app", "run", "--host=0.0.0.0", "--port=8000"]