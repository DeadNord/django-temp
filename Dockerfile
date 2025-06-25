# pull official base image
FROM python:3.11.4-slim-buster

# Set the working directory inside the container
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install necessary dependencies for SSH and Git
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*

# Create .ssh directory and set permissions
RUN mkdir -p /root/.ssh && chmod 700 /root/.ssh

# Copy SSH private and public keys from the repo to the container
COPY ./ssh/docker_container_rsa /root/.ssh/id_rsa
COPY ./ssh/docker_container_rsa.pub /root/.ssh/id_rsa.pub

# Set permissions for the SSH keys
RUN chmod 600 /root/.ssh/id_rsa && chmod 644 /root/.ssh/id_rsa.pub

# Add the GitLab server to known hosts to avoid prompt during cloning
RUN ssh-keyscan gitlab.com >> /root/.ssh/known_hosts

# Install Python dependencies
RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy the rest of the project's code into the container
COPY . .

# Collect static files for Django
RUN python ./manage.py collectstatic --noinput

# Command to run the application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--log-level", "debug", "config.wsgi:application"]
