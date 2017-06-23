## caliper-event-analysis: Sending the data to the OpenLRS server

This script is mainly written to send caliper events that stored in the Application Database to the OpenLRS server. We are 
manually extracting the caliper events from the App DB and the script is reading the file containing events one at a time and sends it.
Sample caliper data file is provided in the repo and this file is Delimited by BREAK. The reason for this is some time the caliper data in the APP DB is stored as pretty-print-json and that 
leads to adding a new line character when you do a extract. so care must be taken to get raw JSON format.The Caliper extract of each caliper event consist of Envelope info apart from the data. 

### Requirements 
   1. works with Python 2.7.10 version
   1. pip to download modules
   1. need `request`, `json` module

### Running the script steps:

1. go to the `send_caliper_events.py` and update the variable 

    1. fileToRead = path to event data  
    1. TOKEN =basic auth token
    1. url = OpenLRS end point
    
1. run the script as `python send_caliper_events.py`


This is s bare minimum script to send event data to LRS, Work need to be done taking the token/url from the Properties file and implement proper logging

      
 