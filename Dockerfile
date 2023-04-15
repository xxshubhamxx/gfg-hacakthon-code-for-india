FROM ubuntu:latest

# Update and install dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the application files
COPY . /app

# Install the dependencies
RUN pip3 install -r requirements.txt

# Expose the port
EXPOSE 8080

# Start the application with Gunicorn
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:8080"]