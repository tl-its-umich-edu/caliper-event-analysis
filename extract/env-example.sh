#!/usr/bin/env bash

# Copy this script, change the name of the DB,
# then source it in your shell to set the environment variable before running extract.sh.

##
## DO NOT COMMIT YOUR COPY OF THIS FILE TO THE REPOSITORY
##

MONGODB_ADDRESS=127.0.0.1:27017/remote-db-name; export MONGODB_ADDRESS
