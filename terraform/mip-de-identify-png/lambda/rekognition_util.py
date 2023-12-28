import sys
sys.path.append('lib')
import boto3
from botocore.exceptions import ClientError
import logging

import config


def get_rekognition_client():
    print('get_rekognition_client: profile_name=%s, region_name=%s' % (config.profile_name, config.region_name))

    p_name = None
    if (config.profile_name != ''):
        p_name = config.profile_name
    session = boto3.Session(profile_name=p_name)
    rkg = session.client('rekognition', region_name=config.region_name)
    return rkg


def get_detected_texts_from_s3_object(source_bucket_name, source_object_prefix, source_object_name):
    rkg = get_rekognition_client()
    if rkg is None:
        print('get_detected_texts_from_s3_object: Failed to get rekognition client.')
        return False
    
    config.detected_texts_list = None
    try:
        #Use Amazon Rekognition to detect all of the text in the medical image
        source_object_key = source_object_prefix + source_object_name
        response = rkg.detect_text(Image={'S3Object':{'Bucket':source_bucket_name,'Name':source_object_key}})
        config.detected_texts_list = response['TextDetections']
    except ClientError as e:
        logging.error("get_detected_texts_from_s3_object: unexpected error: ")
        logging.exception(e)
        return False

    if config.detected_texts_list is None:
         print('get_detected_texts_from_s3_object: Failed to get text detections.')
         return False

    #The various text detections are returned in a JSON object.  Aggregate the text into a single large block and
    #keep track of the offsets.  This will allow us to make a single call to Amazon Comprehend Medical for
    #PHI detection and minimize our Comprehend Medical service charges.       
    print ('get_detected_texts_from_s3_object: Aggregating detected text...')

    config.text_block = ""
    config.total_length = 0
    config.offset_array = [0,]
    config.total_offsets = 1

    for detected_text in config.detected_texts_list:
        if detected_text['Type'] == "LINE":
            d_text = detected_text['DetectedText']
            config.text_block = config.text_block + d_text + " " # add detected text plus white space
            config.total_length += len(d_text) + 1 # add text block total length as result of detected text
            config.offset_array.append(config.total_length) # add offset as result of detected text
            config.total_offsets += 1  # increment number of offset array entries by 1 
            print("adding '%s', length: %d, # of offset_array entries: %d" % (d_text+" ", len(d_text) + 1, config.total_offsets))

    return True

