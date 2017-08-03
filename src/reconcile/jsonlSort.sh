#!/bin/sh --

# Execute with arguments:
# 1. (Required) Name of the property to be used for sorting.
# 2. (Optional) Name of the input file to be sorted. Default: stdin

# Improved according to a suggestion from @pkoppstein
# in response to support issue:
# https://github.com/stedolan/jq/issues/1447#issuecomment-314918635

jq --slurp --compact-output --sort-keys 'sort_by(.'${1}')[]' ${2:--}

