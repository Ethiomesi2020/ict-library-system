# Use an official, lightweight Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY app.py .

# Expose port 5000 (the port our Library Flask app runs on)
EXPOSE 5000

# Define the command to run the application
CMD ["python", "app.py"]