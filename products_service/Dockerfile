# Use an official Python base image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY src/ .

# Set environment variables (optional)
ENV PYTHONUNBUFFERED=1

# Expose port if your app runs a server (e.g., FastAPI or Flask)
EXPOSE 8000

# Command to run your app (adjust if using Flask, Django, etc.)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

