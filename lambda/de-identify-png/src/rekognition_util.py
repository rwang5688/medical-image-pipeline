import boto3
from botocore.exceptions import ClientError
import config
import logging


def get_rekognition_client():
    print('get_rekognition_client: profile_name=%s, region_name=%s' % (config.profile_name, config.region_name))

    p_name = None
    if (config.profile_name != ''):
        p_name = config.profile_name
    session = boto3.Session(profile_name=p_name)
    rkg = session.client('rekognition', region_name=config.region_name)
    return rkg


def get_detected_texts_from_s3_object(source_bucket_name, source_prefix, source_object_name):
    rkg = get_rekognition_client()
    if rkg is None:
        print('aggregate_detected_text: Failed to get rekognition client.')
        return False
    
    text_detections = None
    try:
        #Use Amazon Rekognition to detect all of the text in the medical image
        response = rkg.detect_text(Image={'S3Object':{'Bucket':source_bucket_name,'Name':source_prefix+source_object_name}})
        text_detections = response['TextDetections']
    except ClientError as e:
        logging.error("aggregate_detected_text: unexpected error: ")
        logging.exception(e)
        return False

    if text_detections is None:
         print('aggregaate_detected_text: Failed to get text detections.')
         return False
       
    print ('aggregate_detected_text: Aggregating detected text...')

    config.text_block = ""
    config.offset_array = []
    config.total_length = 0
    config.total_offsets = 0

    #The various text detections are returned in a JSON object.  Aggregate the text into a single large block and
    #keep track of the offsets.  This will allow us to make a single call to Amazon Comprehend Medical for
    #PHI detection and minimize our Comprehend Medical service charges.
    for text in text_detections:
        if text['Type'] == "LINE":
            config.offset_array.append(config.total_length)
            config.total_length+=len(text['DetectedText'])+1
            config.text_block=config.text_block+text['DetectedText']+" "
            print ("adding '"+text['DetectedText']+"', length: "+str(len(text['DetectedText']))+", offset_array: "+str(config.offset_array))
    config.offset_array.append(config.total_length)
    config.total_offsets = len(config.offset_array)

    return True

