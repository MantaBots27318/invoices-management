#!/bin/bash
# -------------------------------------------------------
# Copyright (c) [2024] FASNY
# All rights reserved
# -------------------------------------------------------
# Script launching code analyze outside of CI/CD
# -------------------------------------------------------
# Nadège LEMPERIERE, @6th november 2024
# Latest revision: 6th november 2024
# -------------------------------------------------------

# Retrieve absolute path to this script
script=$(readlink -f $0)
scriptpath=`dirname $script`

# Use python docker to launch analysis
docker run -it --rm \
       --entrypoint /bin/bash \
       -v $scriptpath/../:/home\
       --workdir /home \
       python:latest \
       /home/scripts/lint.sh
