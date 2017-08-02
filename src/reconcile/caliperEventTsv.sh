#!/bin/sh --

UNSORTED_DATA="unsorted_${$}.tsv"

# Send input through stdin or give a filename as an argument

jq -r '[.generated.attempt.endedAtTime[:19]+"Z", .actor.name, .object["@id"], .generated.value//"0"]|@tsv' ${1:--} > ${UNSORTED_DATA}

sort ${UNSORTED_DATA} | sed 's/%40/@/g'
rm ${UNSORTED_DATA}
