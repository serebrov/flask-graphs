#!/usr/bin/env bash
set -e

SCRIPT_PATH=`dirname $0`

python -m unittest discover -s tests
