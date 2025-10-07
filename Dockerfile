# Dockerfile

# Use the official Python 3.12 slim image as a parent image
FROM python:3.12-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the project files into the container
COPY . .

# Create a non-root user to run the application
RUN adduser --disabled-password --gecos '' --uid 1000 appuser

# Change ownership of the app directory to appuser
RUN chown -R appuser:appuser /app

# Switch to that user
USER appuser
