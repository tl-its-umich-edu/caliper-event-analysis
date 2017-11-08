### Simulate sending caliper events to UDP
 The Unizin Data Platform is intended to absorb the caliper events. UDP is development in progress and this application is taking caliper 1.1 events including envelope from flat files sends it to UDP

### Running requirements
1. The app is tested with Python 3.6.3
2. Install pip from https://pip.pypa.io/en/latest/installing/#install-pip to download some of the python module that are outside of standard python library.
3. To install the required modules for the utility do `pip install -r requirements.txt`

### Run 
 The last argument if not provided default to 1 run
 `python3 main.py <path-to properties-file> <path-to-json-events-directory> <number-of-times-to-run-Json-Events>` 


###### Docker local Run
 First a docker build needed and then running the build in container. 
 If the build image changes a new name needs to be given like `simulator1` or delete the old build images to use the same name
1. Build the images first  ` docker build -t simulator .` 
2. Run image in a container `docker run -it --rm --name simulator-run simulator`

##### Running in OpenShift
1. Connect to OpenShift via command line.
    1. Download the client from the Openshift command line [link](https://openshift.dsc.umich.edu:8443/console/command-line) and extract it
    2. copy it to a location on the Path on your Mac (`cp oc /usr/local/bin` - you may need to be an admin on your computer)
    3. From time to time open shift instance is upgraded so its highly recommended to get the latest OS client from the 
       [here](https://openshift.dsc.umich.edu:8443/console/command-line`) as some of the commands work If the openShift 
       Client version is in sync with the Openshit server version. 
    4. log into the CLI using the same session token from [here](https://openshift.dsc.umich.edu:8443/console/command-line)
    5. select project as `oc project oc simulator-dev`
2. ###### secrets
    the app needs property file and a directory containing json files these are made as secrets so one can have a option to change
    1. secrets Managemnent
       1. creating `oc create secret generic <secret-name> --from-file=<secret-file/s>`
            1. `oc create secret generic config --from-file=config.yml`
            2. `oc create secret generic events --from-file=events/`
       2. deleting
            1. First, take a look at the existing secrets `oc get secrets` 
            2. Actually deleting them as `oc secret <secret-name>`
3. First step is build in the OpenShift, Goto build [page](https://openshift.dsc.umich.edu:8443/console/project/simulator-dev/browse/builds/simulator) start the build by clicking 'StartBuild' 
    do it from command line as `oc start-build simulator -n simulator-dev --follow`
4. To run the build download the file `pod-batch.yaml`(name can be anything) from the GitHub Repo and run it as
 
        `oc create -f pod-batch.yaml`
   This will create a Pod running the simulator application. checkout the run [here](https://openshift.dsc.umich.edu:8443/console/project/simulator-dev/browse/pods), go to the logs  to check the output of pods. 
   From command line `oc logs pod/<pod-name>` or pull the entire logs to file using `oc logs pod/<pod-name> >logs.txt`
   

###### Notes 

1. Sample properties file `config.yml` and `logging.yml` is placed in the `config` directory. 
2. logs are emitted to the stdout. 

