# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Install curl
RUN apt-get update && apt-get install -y curl

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . /usr/src/app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements/requirements.txt

# Copy the wait-for-selenium script and make it executable
COPY wait-for-selenium.sh /wait-for-selenium.sh
RUN chmod +x /wait-for-selenium.sh

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME World

# Run the wait-for-selenium script, then app.py when the container launches
CMD ["/wait-for-selenium.sh", "selenium:4444", "python", "./app.py"]



# -------

# # Use an official Python runtime as a parent image
# FROM python:3.8-slim

# # Install dependencies required for Chrome
# RUN apt-get update && apt-get install -y \
#   wget \
#   gnupg2 \
#   unzip \
#   libglib2.0-0 \
#   libnss3 \
#   libgconf-2-4 \
#   libfontconfig1 \
#   libxi6 libglu1-mesa \
#   xvfb

# # Download and install Chrome
# RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
#   && dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

# # Download and install Chromedriver
# RUN wget https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip \
#   && unzip chromedriver_linux64.zip \
#   && mv chromedriver /usr/bin/chromedriver \
#   && chmod +x /usr/bin/chromedriver

# # Set display port as an environment variable
# ENV DISPLAY=:99

# # Set the working directory in the container
# WORKDIR /usr/src/app

# # Copy the current directory contents into the container at /usr/src/app
# COPY . /usr/src/app

# # Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements/requirements.txt

# # Make port 8000 available to the world outside this container
# EXPOSE 8000

# # Define environment variable
# ENV NAME World

# # Run app.py when the container launches

# CMD ["python", "./app.py"]
# # CMD ["tail", "-f", "/dev/null"]


# ------------
# # Use an official Python runtime as a parent image
# FROM python:3.8

# # Set the working directory in the container
# WORKDIR /usr/src/app

# # Copy the current directory contents into the container at /usr/src/app
# COPY . /usr/src/app

# # Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements/requirements.txt

# # Make port available to the world outside this container
# EXPOSE 8000

# # Define environment variable
# ENV NAME World

# # Run app.py when the container launches
# CMD ["python", "./app.py"]
