# this is getting the latest under 3.6 version
FROM docker.io/python:3
# Setting the default directory in container
WORKDIR /usr/src/app
# copies requirements.txt from the build source directory into the container
COPY requirements.txt ./
# install the dependencies using Pip
RUN pip3 install --no-cache-dir -r requirements.txt
# copies the app source code to the directory in container
COPY . .
# Running the App takes come configuration files needed for the app
CMD [ "./main.py", "config/config.yml", "events"]
#CMD ['/bin/bash']