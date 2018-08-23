#!/usr/bin/env bash
if [ -z "$PS1" ]; then echo -e "This script must be sourced." ; exit ; fi
source venv/bin/activate
if [[ "$1" == "init" ]]; then
    pip install -r requirements.txt
else
    echo "Did not update dependencies, run with \`source start.sh init\` to update."
fi
export FLASK_APP="app.py"
export FLASK_ENV=development
./app.py
