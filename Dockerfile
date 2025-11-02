# Use an official Python image
FROM python:3.11-slim

# Set working directory in the container
WORKDIR /app

# Copy requirements first (for caching efficiency)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the whole Django project into the container
COPY . .

# Expose port 8000 for Django
EXPOSE 8000

# Run migrations and start Django server
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
