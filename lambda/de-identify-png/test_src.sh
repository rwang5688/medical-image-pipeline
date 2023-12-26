#!/bin/bash
export AWS_REGION=$1

export DPI='72'
export PHI_DETECTION_THRESHOLD='0.00'
export REDACTED_BOX_COLOR='red'

echo "[CMD] python de_identify_png.py"
cd src
python ./de_identify_png.py
cd ..
