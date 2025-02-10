# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set environment variables for Django settings
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies (e.g., SQLite)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy the requirements file to the container and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the Django project into the container
COPY ./tranga-manager /app/

# Expose the port the app will run on
EXPOSE 8000

# Set environment variables for the app (can be overridden when running the container)
ENV DEBUG=False
ENV SECRET_KEY=django-insecure-@lg7fq*-bvgjoq4!voi72uu^d^ki0(o0*lx5fa3fc!fe&2f5xt
ENV ALLOWED_HOSTS=*
ENV DJANGO_EMAIL=default@email.com

# Entry point to run migrations and start Django server with custom configurations
CMD sh -c " \
    # Make database migrations \
    python manage.py makemigrations connector database frontend && \
    # Run database migrations \
    python manage.py migrate && \
    # Create superuser if username and password are passed as environment variables \
    if [ -n \"$DJANGO_USERNAME\" ] && [ -n \"$DJANGO_PASSWORD\" ]; then \
        python manage.py create_custom_superuser \"$DJANGO_USERNAME\" \"$DJANGO_EMAIL\" \"$DJANGO_PASSWORD\"; \
    fi && \
    # Start Django development server with custom port and settings \
    python manage.py collectstatic --noinput && \
    python manage.py runserver 0.0.0.0:8000"

