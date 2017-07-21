#!/bin/sh --

jq -r '[.eventTime[:19]+"Z", .actor.name, .object["@id"], .generated.value//"0"]|@tsv' ${1:-/dev/stdin}
