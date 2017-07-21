#!/bin/sh --

# Send input through stdin or give a filename as an argument

jq -r '[.eventTime[:19]+"Z", .actor.name, .object["@id"], .generated.value//"0"]|@tsv' ${1:--} | \
    sort | sed 's/%40/@/g'
