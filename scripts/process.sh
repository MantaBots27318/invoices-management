#!/bin/bash
# -------------------------------------------------------
# Copyright (c) [2024] FASNY
# All rights reserved
# -------------------------------------------------------
# Script processing ivnoices file in OneDrive folder
# -------------------------------------------------------
# Nadège LEMPERIERE, @6th november 2024
# Latest revision: 6th november 2024
# -------------------------------------------------------

# Retrieve absolute path to this script
script=$(readlink -f $0)
scriptpath=`dirname $script`

# Parse arguments from flags
args=""
while getopts o:p:k: flag
do
    case "${flag}" in
          k) args+=" --token ${OPTARG}";;
          p) args+=" --path ${OPTARG}";;
          o) args+=" --output ${OPTARG}";;
    esac
done

# Create virtual environment
python3 -m venv /tmp/register
. /tmp/register/bin/activate

# Install required python packages
pip install --quiet -r $scriptpath/../requirements.txt

# Launch registration process
python3 $scriptpath/../process.py run $args

# Deactivate virtual environment
deactivate
rm -Rf /tmp/register/

