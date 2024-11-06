#!/bin/bash
# -------------------------------------------------------
# Copyright (c) [2024] FASNY
# All rights reserved
# -------------------------------------------------------
# Script launching pylint analysis
# -------------------------------------------------------
# Nadège LEMPERIERE, @6th November 2024
# Latest revision: 6th November 2024
# -------------------------------------------------------

# Retrieve absolute path to this script
script=$(readlink -f $0)
scriptpath=`dirname $script`

# Install required python packages
pip install --quiet --no-warn-script-location -r $scriptpath/../requirements-test.txt
pip install --quiet --no-warn-script-location -r $scriptpath/../requirements.txt

# Launch pylint analysis
pylint --rcfile=$scriptpath/../.pylintrc $scriptpath/../process.py