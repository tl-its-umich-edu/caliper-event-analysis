FROM python:3
WORKDIR /usr/src/app
RUN ls -la
RUN pwd
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt
RUN ls -la
RUN pwd
COPY . .
RUN ls -la
RUN pwd
ENTRYPOINT [ "./main.py", "config/config.yml", "events"]
#CMD ['/bin/bash']