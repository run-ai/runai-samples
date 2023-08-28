#!/bin/bash

# Clone a GIT repo into the running container into a specific directory
git clone https://github.com/wcarrollrai/containers-demo /home/jovyan/work

# Install any python packages cloned from the repo
pip install -r /home/jovyan/work/requirements.txt

# Run Jupyter lab and allow for RunAI added parameters
jupyter lab --port=8888 --ip=0.0.0.0 --allow-root $1 $2 $3