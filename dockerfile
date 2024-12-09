# Use the official Python image from the Docker Hub
FROM python:3.12.4-bookworm

# Install necessary dependencies
RUN apt-get update && \
    apt-get install -y libreoffice poppler-utils 

# Set environment variables to prevent Python from writing pyc files to disc and to prevent Python from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Expose the port Streamlit is running on
EXPOSE 8090

# Copy and execute the entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Run the entrypoint script
CMD ["/entrypoint.sh"]
