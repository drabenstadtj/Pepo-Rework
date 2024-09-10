# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Default command will be overwritten in docker-compose for Celery worker and Celery beat
CMD ["celery", "-A", "tasks", "worker", "--loglevel=info"]
