#!/bin/bash
rm -rf ./zip && mkdir zip

cd ./src
git archive -o dcm-to-png.zip HEAD dcm_to_png.py \
    bin numpy numpy.libs PIL pydicom
mv dcm-to-png.zip ../zip

cd ..

