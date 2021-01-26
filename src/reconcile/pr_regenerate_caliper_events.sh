#!/bin/sh --

# Send input on stdin or give the name of an input file as the first argument
jq --compact-output --sort-keys --from-file pr_caliper_event_template.jq ${1:--}
