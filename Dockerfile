# Dockerfile for FastAPI with Poetry and Prisma
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV POETRY_VERSION=1.7.1
ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PATH="$POETRY_HOME/bin:$PATH"

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml poetry.lock* ./

# Install dependencies
RUN poetry install --no-interaction --no-ansi --no-root

# Copy Prisma schema
COPY schema.prisma ./

# Generate Prisma Client
RUN poetry run prisma db push --accept-data-loss && poetry run prisma generate

# Copy application code
COPY . .

# Expose port
EXPOSE 8001

# Command to run the application
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

