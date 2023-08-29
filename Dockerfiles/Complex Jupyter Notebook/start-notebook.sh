#!/bin/bash
set +euo pipefail

# Activate the Conda Environments
source /opt/conda/bin/activate

# Run a Jupyter 
jupyter lab --port=8888 --ip=0.0.0.0 --allow-root $1 $2 $3

