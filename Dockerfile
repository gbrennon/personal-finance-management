# Dockerfile

# Use the official Python 3.12 slim image as a parent image
FROM python:3.12-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# --- ADDED STEP: Upgrade pip to the latest version ---
RUN python -m pip install --upgrade pip

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the project files into the container
COPY . .
