#!/bin/bash

# Source this file to load the credentials to your environment.

TR2YT_ROOT=$(pwd)

 if [ ! -f "${TR2YT_ROOT}/asset/README.md" ]; then
     echo "Error: Please run this script from the root of the repository."
     exit 1
 fi

source "${TR2YT_ROOT}/credentials.sh"

export PYTHONPATH=${PYTHONPATH}:${TR2YT_ROOT}/
