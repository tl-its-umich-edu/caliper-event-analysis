#!/usr/bin/env bash

# Copy this script, change the remote user and host,
# then run it to open a local tunnel to the remote MongoDB service.

##
## DO NOT COMMIT YOUR COPY OF THIS FILE TO THE REPOSITORY
##

ssh -Nv -L127.0.0.1:27017:0.0.0.0:27017 remote-user@remote-host.example.org
