# caliper-event-analysis: Reconcile events between eventstore and application

## Preparation

### Application log file

Prepare log files from the application with as much data
as possible to properly identify the Caliper events.  In
the case of Problem Roulette (PR), those items are:

* **Timestamp** (`.eventTime`): Must be UTC time
in ISO 8601 format.  Note that PR doesn't include
fractional seconds in its timestamps.
* **Actor** (`.actor.name`): The users' U-M uniqnames or email
address for users with Friend accounts.
PR created Caliper events with uniqname or email address in the
`.actor.name` property. other applications may only put it
in the `.actor.@id` property.  Note that email addresses
will have special characters encoded (e.g., `@` is encoded
as `%40`).
* **Object ID** (`.object.@id`): The resource which the
actor acted upon.  PR used the URL of questions stored
in Google Docs.
* **Answer** (`.generated.value`): The answer the actor
gave for a question.  In the case of events with the
`Completed` action, this value will be a string of a
single digit 1-4.  Events with the `Skipped` action are 
special: they have the value 0 in the log, but the value
`null` (or possibly not present) in Caliper events.

To prepare the given PR log files (TSV) for validation:

1. Remove column headings, the first line of each file.
1. Remove the local time and UID columns.
    ```
    cut -f1,4-
    ```
1. Combine the two log files into one.
1. Sort the combined log file.  Having the timestamp at
the beginning of the line is convenient.
    ```
    sort
    ```

### Caliper events

Create a file of data from the Caliper events that matches the
format of the application log file.  TSV is a convenient format
for this purpose and is easier to work with than CSV.

1. Get all events with the `Completed` or `Skipped` action.
    ```
    fgrep -e 'action#Completed' -e 'action#Skipped'
    ```
    (Or other similar command.)
    
    Avoid regular expressions as
    they are much slower to evaluate.  When regexes aren't
    needed, `fgrep` is faster than `grep` in most cases.
1. Get the same properties from events in the same order
as they appear in the PR log.
    ```
    jq -r '[.eventTime[:19]+"Z", .actor.name, .object["@id"], .generated.value//"0"]|@tsv'
    ```
    In this example, the fractional seconds are truncated from
    `.eventTime`, "0" is output if `.generated.value` is null
    or missing, and the output is formatted as TSV.
1. Some actor names may be email addresses, but `@` has been
encoded as `%40`, so decode them back.
    ```
    sed 's/%40/@/g'
    ```
    This is not ideal.  Other characters may also need
    decoding.  Unfortunately, jq doesn't have a decode
    function, so it must be done in an additional step,
    like this.
1. Sort the event data file.  Having the timestamp at
the beginning of the line is convenient.
    ```
    sort
    ```

>### ℹ️ Notes about duplicate lines
>Depending on the goal of the comparison, it may be desirable to 
remove duplicate lines from the log and event data files.  Do this
while sorting the files:
>```
>sort -u
>```
>To remove duplicate lines from a file that's already been sorted:
>```
>sort -m -u
>```
>(The `uniq` utility can remove duplicate lines from a sorted file,
but the above command is usually much faster.)
>
> `jq -Rr '(./" ")|.[-1]/"\t"+.[-2:-1]|@tsv'
`

## Processing

Once the application log file (`log.tsv`) and the event data file
(`event.tsv`) are ready, comparing them is a simple matter of running
them through the `comm` utility.

### Missing Caliper events

To get only the log file lines that didn't match any lines of the
event data file:
```
comm -23 log.tsv event.tsv > missing.tsv
```

### Unlogged Caliper events

To get only the event data file lines that didn't match any lines of the
log file:
```
comm -13 log.tsv event.tsv > unlogged.tsv
```

### Matching Caliper events

To get only the log file lines that matched any lines of the
event data file:
```
comm -12 log.tsv event.tsv > matches.tsv
```

>### ⚠️ Combine comparison results to save time
>Although the `comm` utility runs very quickly, it may save time
to save the combination of the previous three comparisons in one file,
then extract the lines needed from that file.
>
> **_Note_**: `comm` apparently doesn't append column delimiters to
lines that have values in only columns 1 or 2!
>
>* Save the combined results
>    ```
>    comm --output-delimiter=\| log.tsv event.tsv > comm-all.txt 
>    ```
>* Get a column from combined results, for example, lines that
appear only in the log file (i.e., missing Caliper events)
>    ```
>    cut -d\| -f1 comm-all.txt | fgrep .
>    ```


In this 

Running time: 0m3.5s


1st comm run
1523  2017-07-16T04:37:28Z: nohup comm -23 log.tsv event.tsv > missing.tsv &
-rw-rw-r--. 1 centos centos 104929677 Jul 16 04:37 missing.tsv


2nd tsvEvent.sh run
-rw-rw-r--. 1 centos centos 142851885 Jul 17 04:59 event.tsv 
$ cat event.start
Mon Jul 17 04:55:46 UTC 2017

2nd comm run
Mon Jul 17 11:10:37 UTC 2017
Mon Jul 17 11:10:44 UTC 2017