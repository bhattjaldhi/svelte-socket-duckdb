FROM python:3.11-slim

WORKDIR /app

# Copy requirements file
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip

# Install dependencies
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Install Gunicorn
RUN pip install gunicorn

# Expose port 5000
EXPOSE 5000

# Start the application with Gunicorn
CMD ["gunicorn", "-w", "4", "-k", "eventlet", "-b", "0.0.0.0:5000", "app:app"]
