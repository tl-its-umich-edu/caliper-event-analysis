### Simulate sending caliper events to UDP
 The Unizin Data Platform is intended to absorb the caliper events. UDP is development in progress and this application is taking caliper 1.1 events including envelope from flat files sends it to UDP

### Running requirements
1. The script is tested with Python 3.6.3
2. Install pip from https://pip.pypa.io/en/latest/installing/#install-pip to download some of the python module that are outside of standard python library.
3. To install the required modules for the utility do pip install -r requirements.txt

### Run 
 `python3 main.py <path-to properties-file> <path-to-json-events-directory> <number-of-times-to-send-static-events>`
 
 The application takes 3 command line arguments 
  1. properties that contains sample user/course data also endpoint credentials. 
  2. A directory path that contains sample of 5 json events from leccap application
  3. A number representing the number of time to send the same sample events to the Endpoint
  

###### Notes 

1. Sample properties file `config.yml` and `logging.ini` is placed in the config directory. 
2. logs can be emitted to the stdout or to a file. The default logs is at the `/log` 