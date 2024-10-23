# Use the official Python image from Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY Yoga/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the working directory
COPY . .

# Set environment variables for Django
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Ensure media directory is created (if needed)
RUN mkdir -p /app/media/poses

# Collect static files
RUN python Yoga/manage.py collectstatic --noinput


# Expose the port the app runs on
EXPOSE 8000

feature/docker-setup
# Run migrations
RUN python Yoga/manage.py migrate --noinput

# Start the Django application
CMD ["python", "Yoga/manage.py", "runserver", "0.0.0.0:8000"]
