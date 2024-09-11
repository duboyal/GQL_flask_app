# Use an official Node runtime as a parent image
FROM node:16-alpine

# Set the working directory in the container
WORKDIR /app

# Copy the package.json and package-lock.json files into the container
COPY package.json ./
COPY package-lock.json ./

# Install any dependencies specified in package.json
RUN npm install --verbose

# Copy the rest of the application code into the container at /app
COPY . .

# Make port 3000 available to the world outside this container
EXPOSE 3000

# Define the environment variable for development
ENV NODE_ENV=development

# Define the command to run the application
CMD ["npm", "start"]


# # Use an official Node runtime as a parent image
# FROM node:16-alpine

# # Set the working directory in the container
# WORKDIR /app

# # Copy the package.json and package-lock.json files into the container
# COPY package.json ./
# COPY package-lock.json ./

# # Install any dependencies specified in package.json
# RUN npm install --verbose

# # Copy the rest of the application code into the container at /app
# COPY . .

# # Make port 3000 available to the world outside this container
# EXPOSE 3000

# # Define the environment variable for development
# ENV NODE_ENV=development

# # Define the command to run the application
# CMD ["npm", "start"]



