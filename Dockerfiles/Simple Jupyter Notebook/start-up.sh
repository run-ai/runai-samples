#!/bin/bash

git clone https://github.com/wcarrollrai/containers-demo /home/jovyan/work

pip install -r /home/jovyan/work/requirements.txt

jupyter lab --port=8888 --ip=0.0.0.0 --allow-root $1 $2 $3