# Pull the official base image
FROM python:3.8-slim-buster

# Install system-level dependencies for pycairo
RUN apt-get update && apt-get install -y \
    libcairo2 \
    libgirepository1.0-dev \
    gir1.2-gtk-3.0 \
    libpango1.0-dev \
    libgdk-pixbuf2.0-dev \
    libffi-dev \
    shared-mime-info

# Install PostgreSQL client
RUN apt-get  install -y postgresql-client


# Set environment variables
ENV IN_DOCKER_CONTAINER 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
# Copy .env file
COPY .env /code/
COPY db.sqlite3 /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


# Copy project
COPY . /code/

# Expose port 8000
EXPOSE 8000

# Start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]