#!/bin/bash

python3 run.py &

cd unified-planning/notebooks

jupyter notebook --port=8062 --no-browser --ip=0.0.0.0 --allow-root --NotebookApp.token='' --NotebookApp.password=''
