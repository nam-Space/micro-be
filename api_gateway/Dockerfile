# Use official Python image
FROM python:3.12

# Set working directory inside the container
WORKDIR /app

# Copy project files into container
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port Django will run on
EXPOSE 8001

# Run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
