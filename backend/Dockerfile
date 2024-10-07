# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Create logs directory and set permissions
RUN mkdir -p /app/logs && chmod -R 777 /app/logs

# Install the dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Install Gunicorn for production use
RUN pip install gunicorn

# Use Gunicorn as the default command for production
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "run:app"]
