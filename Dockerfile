#Use an official Python runtime as a parent image
FROM python:3.12-slim

#Set the working directory in the container
WORKDIR /app

#Copy the application code into the container
COPY appweb/ /app/appweb/
COPY requirements.txt /app/

#Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

#Expose port 8080
EXPOSE 8080

#Run the Flask app
CMD ["python", "appweb/apprun.py"]


