#!/bin/sh --

# Execute with an argument containing the name of the property to be
# used for sorting.

# Improved according to a suggestion from @pkoppstein in response to my
# support issue:
# https://github.com/stedolan/jq/issues/1447#issuecomment-314918635

jq --slurp --compact-output 'sort_by(.'${1}')[]'

