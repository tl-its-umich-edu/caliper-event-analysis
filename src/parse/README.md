## caliper-event-analysis: Formatting the event data extracted from the Application Database for the dropped data

This script is mainly written for the ProblemRoulette event that stored in the Database, So if the data contains \n 
and lot of spaces/tab. This script removes all those thing. 

### Running the script steps:

1. go to the `parsing.py` and update the variable `fileToRead` = path to event data that needs to be formatted also update 
   `fileToWrite`= path to event data write to after formatting
1. run the script as `python parsing.py`

      
 