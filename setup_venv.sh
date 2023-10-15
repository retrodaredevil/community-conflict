#!/usr/bin/env bash
set -e
BASEDIR=$(dirname "$0")
cd "$BASEDIR"

python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
