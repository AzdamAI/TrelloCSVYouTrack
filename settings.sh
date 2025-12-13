#!/bin/bash

# Source this file to load the credentials to your environment.

TRCSVYT_ROOT=$(pwd)

if [ ! -f "${TRCSVYT_ROOT}/README.md" ]; then
    echo "Error: Please run this script from the root of the repository."
    exit 1
fi

# Ensure assets directory exists for CSV inputs/outputs
mkdir -p "${TRCSVYT_ROOT}/assets"

source "${TRCSVYT_ROOT}/credentials.sh"

export PYTHONPATH=${PYTHONPATH}:${TRCSVYT_ROOT}/
