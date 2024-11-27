# Use the official python image as the base image
FROM python:3.9-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements files to the working directory
COPY requirements.txt .

# install the required python package
RUN pip3 install --no-cache-dir -r requirements.txt

# copy the application code to the working directory
COPY . .

# Set the environment variable fo the flask app
ENV FLASK_RUN_HOST=0.0.0.0

#Expose the port in which the flask app will run
EXPOSE 5000

# Start the flask app when the container is run
CMD ["flask", "run"]