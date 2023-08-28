#!/bin/bash
set +euo pipefail

source /opt/conda/bin/activate
jupyter lab --port=8888 --ip=0.0.0.0 --allow-root $1 $2 $3

