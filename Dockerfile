# Use an official Python runtime as a base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install dependencies
COPY Yoga/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project into the container
COPY . /app
# COPY . .

# Set environment variables for Django
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Collect static files
RUN mkdir -p /app/static /app/media
RUN python Yoga/manage.py collectstatic --noinput

# Run migrations
RUN python Yoga/manage.py migrate --noinput

CMD ["python", "Yoga/manage.py", "runserver", "0.0.0.0:8000"]
