#!/bin/bash
rm -rf ./zip && mkdir zip

cd ./src
git archive -o de-identify-png.zip HEAD de_identify_png.py \
    bin numpy numpy.libs PIL pydicom
mv data-k12-fetch-s3-data.zip ../zip

cd ..

