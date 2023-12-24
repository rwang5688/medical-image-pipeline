#!/bin/bash
export AWS_REGION=$2

export SOURCE_DATA_BUCKET_NAME='aws-edu-cop-data-demo-datasets'
export SIS_DEMO_MOCK_DATA_PREFIX='data-k12/v1/mockdata/sis_demo_parquet/'
export LMS_DEMO_MOCK_DATA_PREFIX='data-k12/v1/mockdata/lms_demo/v1/'
export RAW_DATA_BUCKET_NAME='data-k12-raw-'$1'-test'
export SIS_DEMO_RAW_DATA_PREFIX='sisdb/sisdemo/'
export LMS_DEMO_RAW_DATA_PREFIX='lmsapi/'

echo "[CMD] python data_k12_fetch_demo_data.py"
cd src
python ./data_k12_fetch_demo_data.py
cd ..
