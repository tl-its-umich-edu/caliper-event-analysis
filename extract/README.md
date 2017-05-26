# caliper-event-analysis: Extract Events From the LRS' DB

## Open an SSH tunnel to the LRS' DB _(optional)_ 

If the LRS' MongoDB service is on a protected network (e.g., behind a 
firewall), use SSH to connect to its server and open a tunnel to the
service to make it appear to be available locally.

1. `cp tunnel-example.sh tunnel-.sh`
1. Edit `tunnel-.sh`
    1. Change `remote-user` to the username on the server.
    1. Change `remote-host.example.org` to the hostname of the server.
1. Run `tunnel-.sh` to set up the tunnel
    1. Consider the requirements for connecting to the server
        specified in the script before running it.
        (E.g., you may need to use a VPN or other security features.)
       1. VPN:  If you need to use a VPN to connect to the server, 
          start the VPN client before running the script.
       1. PEM authentication:  If you need to use PEM files to
          authenticate to the server, put the files in an
          appropriate, secure place that can be accessed by the
          script.  Possible ways to use the PEM files:
          1. Add the `-i` option to the script and give the path to
            the PEM file as an argument.  See OpenSSH
            [`-i` documentation](http://man.openbsd.org/ssh#i) 
            for more information.
          1. In your `~/.ssh/config` file, add a `Host` keyword with
              a pattern to match the hostname and a `IdentityFile`
              keyword with the path to the PEM file.  See OpenSSH
              [`IdentityFile` documentation](http://man.openbsd.org/ssh_config#IdentityFile)
              for more information.
    1. The tunnel will make the remote service appear to be local,
        responding to the address `127.0.0.1:27017/remote-db-name`.
    1. The script displays verbose output to allow monitoring the
        connection and to make it easy to close the tunnel later.
    1. Since this script occupies a terminal, it's best to run the
        following commands in another terminal.
        
## Set the LRS' DB address in the environment _(optional)_ 

The `extract` program can be given the address of the LRS' DB using
a command line option.  However, it may be more convenient to set
the address in the `MONGODB_ADDRESS` environment variable.  This is
especially true if `extract` will be run interactively rather than as
a batch process.

1. `cp env-example.sh env-.sh`
1. Edit `env-.sh`
    1. Change `remote-db-name` to the name of the LRS' MongoDB on the
        server.
1. Run `source env-.sh` to set up the tunnel
    1. Using the `source` command is required to set the environment
        variable in the current shell.
1. After the LRS' DB address is set in the environment, it's not
    necessary to specify the address to the `extract` program on the
    command line.  However, if the address is given on the command line,
    it will override any value set in the environment.

## Run the `extract` program

After the options above have been chosen, if any, `extract` should be 
ready to run.  The program accepts two command line options:

* **`-h <host>`**

    MongoDB host to query. (Format: `hostName:portNum/dbName`)
    
    Default: `127.0.0.1:27017/test`
    
    The default comes from the `mongo` program.  It 
        may be overridden by setting env. variable
        MONGODB_ADDRESS.  If a host is given using this option,
        it overrides any value in the env. variable.

* **`-n <num_events>`**

    Number of most recent events to extract.

    Default: 1

> ℹ️ Note that `extract` currently uses a hard-coded query to extract events emitted
> from a specific application that includes the string "problemroulette" in the JSON.
> A future update will add an option to `extract` to allow specification of a
> different query. 

The output of `extract` will be one JSON object per line.  This is known
as the [JSON Lines](http://jsonlines.org/) format.  This format makes further 
processing of the events with command line tools easier.  The usual 
filename extension for this format is `.jsonl`.

## Example

In the first terminal, set up the tunnel:

```
$ ./tunnel-.sh
OpenSSH_7.4p1, LibreSSL 2.5.0
debug1: Reading configuration data /etc/ssh/ssh_config
debug1: Connecting to remote-host.example.org [remote-host.example.org] port 22.
debug1: Connection established.
debug1: Enabling compatibility mode for protocol 2.0
debug1: Local version string SSH-2.0-OpenSSH_7.4
debug1: Remote protocol version 2.0, remote software version OpenSSH_6.6.1p1 Ubuntu-2ubuntu2.8
debug1: match: OpenSSH_6.6.1p1 Ubuntu-2ubuntu2.8 pat OpenSSH_6.6.1* compat 0x04000000
debug1: Authenticating to remote-host.example.org:22 as 'remote-user'
Authenticated to remote-host.example.org ([remote-host.example.org]:22).
debug1: Local connections to 127.0.0.1:27017 forwarded to remote address 0.0.0.0:27017
debug1: Local forwarding listening on 127.0.0.1 port 27017.
...
```

In the second terminal, set the environment and run `extract`:

```
$ source env-.sh
$ ./extract
{"@context":"http://purl.imsglobal.org/ctx/caliper/v1p1","id":"urn:uuid:a438f8ac-1da3-4d48-8c86-94a1b387e0f6","type":"SessionEvent","actor":{"id":"https://example.edu/users/554433","type":"Person"},"action":"LoggedOut","object":{"id":"https://example.edu","type":"SoftwareApplication","version":"v2"},"eventTime":"2016-11-15T11:05:00.000Z","edApp":"https://problemroulette.example.edu","session":{"id":"https://example.edu/sessions/1f6442a482de72ea6ad134943812bff564a76259","type":"Session","user":"https://example.edu/users/554433","dateCreated":"2016-11-15T10:00:00.000Z","startedAtTime":"2016-11-15T10:00:00.000Z","endedAtTime":"2016-11-15T11:05:00.000Z","duration":"PT3000S"}}
```

In this example, `extract` returns only one Caliper event, since that is the default number
of events.

While `extract` runs, log information about the SSH tunnel may appear in the first terminal.

Again in the second terminal, since the `env-.sh` script has already set the DB address in
the environment, there's no need to do it again before another run of `extract`:

```
$ ./extract -n 5 > events.jsonl
$ cat events.jsonl
{"@context":"http://purl.imsglobal.org/ctx/caliper/v1p1","id":"urn:uuid:a438f8ac-1da3-4d48-8c86-94a1b387e0f6","type":"SessionEvent","actor":{"id":"https://example.edu/users/554433","type":"Person"},"action":"LoggedOut","object":{"id":"https://example.edu","type":"SoftwareApplication","version":"v2"},"eventTime":"2016-11-15T11:05:00.000Z","edApp":"https://problemroulette.example.edu","session":{"id":"https://example.edu/sessions/1f6442a482de72ea6ad134943812bff564a76259","type":"Session","user":"https://example.edu/users/554433","dateCreated":"2016-11-15T10:00:00.000Z","startedAtTime":"2016-11-15T10:00:00.000Z","endedAtTime":"2016-11-15T11:05:00.000Z","duration":"PT3000S"}}
{"@context":"http://purl.imsglobal.org/ctx/caliper/v1p1","id":"urn:uuid:3bdab9e6-11cd-4a0f-9d09-8e363994176b","type":"AnnotationEvent","actor":{"id":"https://example.edu/users/554433","type":"Person"},"action":"Shared","object":{"id":"https://example.com/#/texts/imscaliperimplguide","type":"Document","name":"IMS Caliper Implementation Guide","version":"1.1"},"generated":{"id":"https://example.com/users/554433/texts/imscaliperimplguide/shares/1","type":"SharedAnnotation","annotator":"https://example.edu/users/554433","annotated":"https://example.com/#/texts/imscaliperimplguide","withAgents":[{"id":"https://example.edu/users/657585","type":"Person"},{"id":"https://example.edu/users/667788","type":"Person"}],"dateCreated":"2016-11-15T10:15:00.000Z"},"eventTime":"2016-11-15T10:15:00.000Z","edApp":{"id":"https://problemroulette.example.com/reader","type":"SoftwareApplication","name":"ePub Reader","version":"1.2.3"},"group":{"id":"https://example.edu/terms/201601/courses/7/sections/1","type":"CourseSection","courseNumber":"CPS 435-01","academicSession":"Fall 2016"},"membership":{"id":"https://example.edu/terms/201601/courses/7/sections/1/rosters/1","type":"Membership","member":"https://example.edu/users/554433","organization":"https://example.edu/terms/201601/courses/7/sections/1","roles":["Learner"],"status":"Active","dateCreated":"2016-08-01T06:00:00.000Z"},"session":{"id":"https://example.com/sessions/1f6442a482de72ea6ad134943812bff564a76259","type":"Session","startedAtTime":"2016-11-15T10:00:00.000Z"}}
{"@context":"http://purl.imsglobal.org/ctx/caliper/v1p1","id":"urn:uuid:d4618c23-d612-4709-8d9a-478d87808067","type":"AnnotationEvent","actor":{"id":"https://example.edu/users/554433","type":"Person"},"action":"Bookmarked","object":{"id":"https://example.com/#/texts/imscaliperimplguide/cfi/6/10!/4/2/2/2@0:0","type":"Page","name":"IMS Caliper Implementation Guide, pg 5","version":"1.1"},"generated":{"id":"https://example.com/users/554433/texts/imscaliperimplguide/bookmarks/1","type":"BookmarkAnnotation","annotator":"https://example.edu/users/554433","annotated":"https://example.com/#/texts/imscaliperimplguide/cfi/6/10!/4/2/2/2@0:0","bookmarkNotes":"Caliper profiles model discrete learning activities or supporting activities that facilitate learning.","dateCreated":"2016-11-15T10:15:00.000Z"},"eventTime":"2016-11-15T10:15:00.000Z","edApp":{"id":"https://problemroulette.example.com/reader","type":"SoftwareApplication","name":"ePub Reader","version":"1.2.3"},"group":{"id":"https://example.edu/terms/201601/courses/7/sections/1","type":"CourseSection","courseNumber":"CPS 435-01","academicSession":"Fall 2016"},"membership":{"id":"https://example.edu/terms/201601/courses/7/sections/1/rosters/1","type":"Membership","member":"https://example.edu/users/554433","organization":"https://example.edu/terms/201601/courses/7/sections/1","roles":["Learner"],"status":"Active","dateCreated":"2016-08-01T06:00:00.000Z"},"session":{"id":"https://example.com/sessions/1f6442a482de72ea6ad134943812bff564a76259","type":"Session","startedAtTime":"2016-11-15T10:00:00.000Z"}}
{"@context":"http://purl.imsglobal.org/ctx/caliper/v1p1","id":"urn:uuid:ff9ec22a-fc59-4ae1-ae8d-2c9463ee2f8f","type":"NavigationEvent","actor":{"id":"https://example.edu/users/554433","type":"Person"},"action":"NavigatedTo","object":{"id":"https://example.edu/terms/201601/courses/7/sections/1/pages/2","type":"WebPage","name":"Learning Analytics Specifications","description":"Overview of Learning Analytics Specifications with particular emphasis on IMS Caliper.","dateCreated":"2016-08-01T09:00:00.000Z"},"eventTime":"2016-11-15T10:15:00.000Z","referrer":{"id":"https://example.edu/terms/201601/courses/7/sections/1/pages/1","type":"WebPage"},"edApp":"https://problemroulette.example.edu","group":{"id":"https://example.edu/terms/201601/courses/7/sections/1","type":"CourseSection","courseNumber":"CPS 435-01","academicSession":"Fall 2016"},"membership":{"id":"https://example.edu/terms/201601/courses/7/sections/1/rosters/1","type":"Membership","member":"https://example.edu/users/554433","organization":"https://example.edu/terms/201601/courses/7/sections/1","roles":["Learner"],"status":"Active","dateCreated":"2016-08-01T06:00:00.000Z"},"session":{"id":"https://example.edu/sessions/1f6442a482de72ea6ad134943812bff564a76259","type":"Session","startedAtTime":"2016-11-15T10:00:00.000Z"}}
{"@context":"http://purl.imsglobal.org/ctx/caliper/v1p1","id":"urn:uuid:fcd495d0-3740-4298-9bec-1154571dc211","type":"SessionEvent","actor":{"id":"https://example.edu/users/554433","type":"Person"},"action":"LoggedIn","object":{"id":"https://example.edu","type":"SoftwareApplication","version":"v2"},"eventTime":"2016-11-15T10:15:00.000Z","edApp":"https://problemroulette.example.edu","session":{"id":"https://example.edu/sessions/1f6442a482de72ea6ad134943812bff564a76259","type":"Session","user":"https://example.edu/users/554433","dateCreated":"2016-11-15T10:00:00.000Z","startedAtTime":"2016-11-15T10:00:00.000Z"}}
```

In this example, the `-n` option was used to specify that the five most recent events should
be returned.  They were redirected to a file to show the use of the `.jsonl` filename
extension.  Examination of the file with `cat` shows that each line contains only one JSON
object, with only a line break between them.
