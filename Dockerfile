# Use the official Python image as the base image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the application files to the container
COPY . .
COPY .env .env
COPY gcreds.json gcreds.json

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port (Cloud Run will override this)
EXPOSE 8080

# Command to run the app with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "run:app"]
