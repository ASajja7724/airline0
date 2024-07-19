# Use the official Python 3 image from the Docker Hub
FROM python:3
# Copy the current directory contents into the container at /usr/src/app
COPY .  /usr/src/app
# Set the working directory in the container
WORKDIR /usr/src/app
# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt
# Run manage.py when the container launches
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
