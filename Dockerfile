# use another docker file - python 3
FROM python:3
# get everthing in this application and store in follwing container  
COPY .  /usr/src/app
# go into the following directory
WORKDIR /usr/src/app
# install all needed addons
RUN pip install -r requirements.txt
# run the follwing commands
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
