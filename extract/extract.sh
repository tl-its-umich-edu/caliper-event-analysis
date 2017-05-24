#!/usr/bin/env bash

usage() {
    cat 1>&2 <<-EOT # This heredoc must be indented with tabs, not spaces
	Usage: $0 [-h <host>] [-n <num_events>]

	Where:
	    -h      MongoDB host to query.  (Format: "hostName:portNum/dbName")
	            Default if not given: 127.0.0.1:27017/test
	            The default may be overridden by setting env. variable MONGODB_ADDRESS

	    -n      Number of most recent events to extract.
	            Default: 1
	EOT
    exit 1
}

while getopts ":h:n:" option; do
    case "${option}" in
        h)
            optionMongoDbAddress=${OPTARG}
            ;;
        n)
            optionNumEvents=${OPTARG}
            ;;
        *)
            usage
            ;;
    esac
done
shift $((OPTIND-1))

# Get name of MongoDB service from commandline option or environment variable MONGODB_ADDRESS.
mongoDbAddress="${optionMongoDbAddress:-${MONGODB_ADDRESS}}"
numEvents="${optionNumEvents:-1}"

mongo --quiet ${mongoDbAddress} --eval "var numEvents=${numEvents};" extract.js


