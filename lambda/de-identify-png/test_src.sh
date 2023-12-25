#!/bin/bash
export AWS_REGION=$1

echo "[CMD] python de_identify_png.py"
cd src
python ./de_identify_png.py
cd ..
