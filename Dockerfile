# Base image
FROM python:3.11

# Create app directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source code
COPY . .

# Command to run the service
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]