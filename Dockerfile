# Dockerfile

# Use the official Python 3.12 slim image as a parent image
FROM python:3.12-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies required for building Python packages (e.g., packages with C extensions)
# We install and immediately clean up the build tools in the same layer to keep the final image size small.
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && apt-get autoremove -y build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user to run the application securely. 
# We use a fixed UID (1000) for consistency, which is often the first non-root user.
RUN adduser --disabled-password --gecos '' --uid 1000 appuser

# Set the working directory in the container
WORKDIR /app

# Change ownership of the working directory to appuser before switching users.
# This ensures 'appuser' has full permissions to read/write in /app.
RUN chown -R appuser:appuser /app

# Switch to the non-root user. All subsequent commands (RUN, CMD) will execute as 'appuser'.
USER appuser

# Upgrade pip to the latest version. Installing into the user's home directory.
RUN python -m pip install --upgrade pip --user

# Copy the requirements file and install dependencies.
# The --chown flag ensures the file is owned by the correct user immediately.
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --user -r requirements.txt

# Add the user's local bin directory (where 'pip install --user' places executables) to PATH
ENV PATH="/home/appuser/.local/bin:${PATH}"

# Copy the rest of the project files into the container
COPY --chown=appuser:appuser . .

# Expose port 8000
EXPOSE 8000

# Default command (runs as appuser)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]