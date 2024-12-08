# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application code into the container
COPY appweb/ /app/appweb/
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port (optional for documentation)
EXPOSE 8080

# Run the application, resolving the PORT variable at runtime
CMD ["python", "-m", "waitress", "--port=${PORT}", "appweb.apprun:app"]

