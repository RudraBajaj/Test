# Use an official Python runtime as a parent image
# Using Python 3.11 for better discord.py voice compatibility
FROM python:3.11-slim

# Set the working directory in the container to /app
WORKDIR /app

# Install FFmpeg and clean up in one layer to reduce image size
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt /app/

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . /app

# Run main.py when the container launches
CMD ["python", "main.py"]
