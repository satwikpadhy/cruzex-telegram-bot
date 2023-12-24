# Use an official Python runtime as a base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any dependencies needed by your Python application
RUN pip install --no-cache-dir -r requirements.txt  # If you have a requirements.txt file

# Specify the command to run your application
CMD ["python3", "cruzex-bot.py"]
