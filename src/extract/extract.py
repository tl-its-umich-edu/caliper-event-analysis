#!/usr/bin/env python

import argparse
import os

PATH_TO_PROGRAM = os.path.dirname(os.path.realpath(__file__))
MONGODB_ADDRESS_ENVVAR = 'MONGODB_ADDRESS'

defaultMongoDbAddress = os.getenv(MONGODB_ADDRESS_ENVVAR, '').strip()

argParser = argparse.ArgumentParser(
    description="Extract events from LRS' MongoDB."
)
argParser.add_argument(
    '--db',
    type=str,
    dest='optionMongoDbAddress',
    metavar=MONGODB_ADDRESS_ENVVAR,
    default=defaultMongoDbAddress,
    help='''MongoDB host to query, as "hostName:portNum/dbName".
        The default may be overridden by setting env. variable {}.
        Default: {}.''' \
        .format(MONGODB_ADDRESS_ENVVAR, '(mongo shell CLI default, usually "127.0.0.1:27017/test")' \
        if defaultMongoDbAddress == '' \
        else '"{}" (set by {} env. variable)'
                .format(defaultMongoDbAddress, MONGODB_ADDRESS_ENVVAR))
)
argParser.add_argument(
    '--num',
    type=int,
    dest='optionNumEvents',
    metavar='NUM_EVENTS',
    default=1,
    help='''Maximum limit of the number of the most recent events to extract.
            Specify a limit of 0 to get all events (use with caution!).
            Default: %(default)s'''
)
argParser.add_argument(
    '--regex',
    type=str,
    dest='optionRawRegex',
    metavar='REGEX',
    default='.*',
    help='''Regular expression used to select events which have a matching value
            in their "raw" property.  The regular expression must be valid for
            use with JavaScript.
            Default: %(default)s'''
)
extractArgs = argParser.parse_args()

os.system(
    "mongo --quiet '{optionMongoDbAddress}' "
    "--eval 'var numEvents={optionNumEvents}; var rawRegex=\"{optionRawRegex}\";' "
    .format(**vars(extractArgs)) +
    "{}/extract.js".format(PATH_TO_PROGRAM)
)
