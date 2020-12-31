#!/usr/bin/env bash

source ~/miniconda3/etc/profile.d/conda.sh
conda activate mesa
nohup python3 gridboltzmann_Viz.py &
