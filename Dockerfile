# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.10.12

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /ninthdjango

# Set the working directory to /music_service
WORKDIR /ninthdjango

# Copy the current directory contents into the container at /music_service
ADD . /ninthdjango/

RUN /usr/local/bin/python -m pip install --upgrade pip

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Copy the startup script into the container
COPY startup.sh .

# Ensure the script is executable
RUN chmod +x startup.sh

# Start the application using the startup script
CMD ["./startup.sh"]