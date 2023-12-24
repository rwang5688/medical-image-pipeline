#!/bin/bash
export AWS_REGION=$1

echo "[CMD] python dcm_to_png.py"
cd src
python ./dcm_to_png.py
cd ..
