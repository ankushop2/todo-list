# Use the official Python image from the Docker Hub
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt requirements.txt

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose port 5002 for the Flask application
EXPOSE 5002

# Run the Flask application
CMD ["python", "main.py"]