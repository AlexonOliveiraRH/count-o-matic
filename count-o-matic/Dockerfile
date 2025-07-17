FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create directories if they don't exist
RUN mkdir -p templates

# Expose the port
EXPOSE 5000

# Run the application using Gunicorn for better performance
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
