### Simulate sending caliper events to UDP
 The Unizin Data Platform is intended to absorb the caliper events. UDP is development in progress and this application is taking caliper 1.1 events including envelope from flat files sends it to UDP

### Running requirements
1. The app is tested with Python 3.6.3
2. Install pip from https://pip.pypa.io/en/latest/installing/#install-pip to download some of the python module that are outside of standard python library.
3. To install the required modules for the utility do `pip install -r requirements.txt`

### Run 
 `python3 main.py <path-to properties-file> <path-to-json-events-directory>` 

###### Notes 

1. Sample properties file `config.yml` and `logging.yml` is placed in the `config` directory. 
2. logs are emitted to the stdout,file. The default logs is at the `/log` 