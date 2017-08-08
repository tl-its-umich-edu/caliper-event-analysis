# caliper-event-analysis: Reconcile events between eventstore and application

## Preparation

### Application log file

Prepare event log files from the application with as much data
as necessary to properly correlate them to Caliper events from
the eventstore.  For example, timestamp, username, event type,
action type, etc.

In the case of Problem Roulette (PR), those items are:

* **Timestamp** (`.eventTime` equivalent): Must be UTC time
in ISO 8601 format.  Note that PR doesn't include
fractional seconds in its timestamps.
* **Username** (`.actor.name` equiv.): The users' U-M uniqnames or
email address for users with Friend accounts. PR created Caliper
events with uniqname or email address in the `.actor.name`
property.  Other applications may only put it in the `.actor.@id`
property.  Note that email addresses will have special characters
encoded (e.g., `@` is encoded as `%40`).
* **Problem ID** (`.object.@id` equiv.): An ID of the problem
which the user answered.  PR used the URL of problems stored
in Google Docs.
* **Answer** (`.generated.value` equiv.): The answer given by
the user for a question.  If the answer is a string of a single
digit 1-4, the Caliper event will have the `Completed` action.
If the answer is the string "0", then the Caliper event will
have the `Skipped` action and the `.generated.value` property
may not be present or it may have the value `null`.

Once the corresponding data items from the application and the
Caliper events have been identified, format the layout of the
application log data.  This same format will be used for the
Caliper event data file later.

Recommendations:

* One event per line.
* Fields are tab delimited and the name of the file should have
a `.tsv` extension.  TSV is a convenient format since the data
probably won't contain tab characters (and is easier to work with
than CSV).
* Each line should begin with the timestamp.
* Sort the lines of the file by timestamp.

### Caliper events

Create a file of data from the Caliper events that matches the
format of the application log file.  Assuming the Caliper events
are in a single, large JSONL file:

1. Get all events with the appropriate `@type` or `action`.  The
basic `grep` utility is a good tool for this purpose.

    For PR, those are events with the `Completed` or `Skipped`
    action.
    ```
    fgrep -e 'action#Completed' -e 'action#Skipped'
    ```
    (Or other similar command.)
    
    Avoid regular expressions as
    they are much slower to evaluate.  When regexes aren't
    needed, `fgrep` is faster than `grep` in most cases.
1. Format the selected event JSON as TSV.  Either use the
`caliperEventTsv.sh` script or follow the steps below.
    1. Get the same properties from events in the same order
    as they appear in the PR log.
        ```
        jq -r '[.eventTime[:19]+"Z", .actor.name, .object["@id"], .generated.value//"0"]|@tsv'
        ```
        In this example, the fractional seconds are truncated from
        `.eventTime` and "0" is output if `.generated.value` is null
        or missing.  Having the timestamp at the beginning of the
        line is convenient for sorting the data.
    1. Sort the event data file.  Having the timestamp at
    the beginning of the line is convenient.
        ```
        sort
        ```
    1. Some actor names may be email addresses, but `@` has been
    encoded as `%40`, so they need to be decoded.
        ```
        sed 's/%40/@/g'
        ```

## Processing

Once the application log file and the event data file (e.g.,
`log.tsv` and `event.tsv`) are ready, reconciling them is a
simple matter of running them through the `comm` utility.

The `reconcile.sh` script can check the input files, reconcile
them, and produce three TSV files of data which represent
missing, unlogged, and matching event data from the files.

See the following sections for explanations of the three
output files and commands for producing the files manually.

### Missing Caliper events

Data from `log.tsv` that was not
found in `event.tsv`.  This may represent a Caliper event that
didn't get stored in the eventstore properly or there was trouble
in sending it.  To get only the log file lines that didn't match
any lines of the event data file:
```
comm -23 log.tsv event.tsv > missing.tsv
```

### Unlogged Caliper events

Data from `event.tsv` that was not
included in `log.tsv`.  This may represent a problem in the
application's logging or maybe events that entered the eventstore
from a different source.  To get only the event data file lines
that didn't match any lines of the log file:
```
comm -13 log.tsv event.tsv > unlogged.tsv
```

### Matching Caliper events

Data that was found in `log.tsv` and `event.tsv`.  To get only
the log file lines that matched any lines of the event data file:
```
comm -12 log.tsv event.tsv > matches.tsv
```
