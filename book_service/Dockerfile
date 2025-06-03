# Use official Python image
FROM python:3.12

# Set working directory inside the container
WORKDIR /app

# Copy project files into container
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python manage.py makemigrations book
RUN python manage.py migrate

# Expose the port Django will run on
EXPOSE 8002

# Run Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8002"]
