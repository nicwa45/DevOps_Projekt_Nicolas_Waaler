# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application code into the container
COPY appweb/ /app/appweb/
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080 to the outside world (using environment variable for flexibility)
EXPOSE ${PORT:-8080}

# Command to run the application using Waitress
CMD ["python", "-m", "waitress", "--port=${PORT:-8080}", "appweb.apprun:app"]
