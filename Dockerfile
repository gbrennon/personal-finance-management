# Dockerfile

# Use the official Python 3.12 slim image as a parent image
FROM python:3.12-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user to run the application
RUN adduser --disabled-password --gecos '' --uid 1000 appuser

# Set the working directory in the container
WORKDIR /app

# Change ownership of the working directory to appuser
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Upgrade pip to the latest version
RUN python -m pip install --upgrade pip --user

# Copy the requirements file and install dependencies
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --user -r requirements.txt

# Add user's local bin to PATH
ENV PATH="/home/appuser/.local/bin:${PATH}"

# Copy the rest of the project files into the container
COPY --chown=appuser:appuser . .

# Expose port 8000
EXPOSE 8000

# Default command (can be overridden by docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]