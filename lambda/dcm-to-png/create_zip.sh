#!/bin/bash
rm -rf ./zip && mkdir zip

cd ./src
git archive -o data-k12-fetch-s3-data.zip HEAD lambda_handler.py \
    bin certifi charset_normalizer idna requests smart_open urllib3
mv data-k12-fetch-s3-data.zip ../zip

cd ..

