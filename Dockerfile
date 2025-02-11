# Use a base image with Python 3.11
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    libssl-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy pyproject.toml and other required files
COPY pyproject.toml README.md LICENSE.md Makefile SECURITY.md /app/

# Install pip, setuptools, wheel, and build
RUN python -m pip install --upgrade pip setuptools wheel build

# Copy the entire project into the container
COPY . /app

# Build the package and install the wheel
RUN python -m build && pip install dist/*.whl

# Keep the container running with a long-running process
CMD ["tail", "-f", "/dev/null"]
