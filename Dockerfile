# Use an official Python runtime as a parent image
FROM python:3.13.0a2-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variable
ENV FLASK_APP=app.py

# Run your Flask app
CMD ["python3", "app.py"]
