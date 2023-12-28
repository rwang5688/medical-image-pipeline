import sys
sys.path.append('lib')
import boto3
from botocore.exceptions import ClientError
import logging

import config


def get_comprehendmedical_client():
    print('get_comprehendmedical_client: profile_name=%s, region_name=%s' % (config.profile_name, config.region_name))

    p_name = None
    if (config.profile_name != ''):
        p_name = config.profile_name
    session = boto3.Session(profile_name=p_name)
    cm = session.client('comprehendmedical', region_name=config.region_name)
    return cm


def get_phi_boxes_list_from_detected_texts():
    cm = get_comprehendmedical_client()
    if cm is None:
        print('get_phi_boxes_list_from_detected_texts: Failed to get comprehendmedical client.')
        return False
    
    config.detected_phi_list = None
    try:
        #Call Amazon Comprehend Medical and pass it the aggregated text from our medical image.
        config.detected_phi_list=cm.detect_phi(Text = config.text_block)
    except ClientError as e:
        logging.error("get_phi_boxes_list_from_detected_texts: unexpected error: ")
        logging.exception(e)
        return False

    if config.detected_phi_list is None:
         print('get_phi_boxes_list_from_detected_texts: Failed to get PHI list.')
         return False
    
    #Amazon Comprehend Medical will return a JSON object that contains all of the PHI detected in the text block with
    #offset values that describe where the PHI begins and ends.  We can use this to determine which of the text blocks 
    #detected by Amazon Rekognition should be redacted.  The 'phi_boxes_list' list is created to keep track of the
    #bounding boxes that potentially contain PHI.
    print ('get_phi_boxes_list_from_detected_texts: Finding PHI text bounding boxes...')

    config.phi_texts_list = []
    config.phi_boxes_list = []
    config.not_redacted = 0

    for phi in config.detected_phi_list['Entities']:
        phi_score = phi['Score']
        phi_text = phi['Text']
        phi_type = phi['Type']
        if phi_score > config.phi_detection_threshold:
            for i in range(0, config.total_offsets-1):
                if config.offset_array[i] <= phi['BeginOffset'] < config.offset_array[i+1]:
                    detected_text = config.detected_texts_list[i]
                    phi_box = detected_text['Geometry']['BoundingBox']
                    if phi_box not in config.phi_boxes_list:
                        print("PHI score = %f: %s was detected as type %s and will be redacted. (BoundingBox = %s)" % (phi_score, phi_text, phi_type, phi_box))
                        config.phi_scores_list.append(phi_score)
                        config.phi_texts_list.append(phi_text)
                        config.phi_types_list.append(phi_type)
                        config.phi_boxes_list.append(phi_box)
        else:
            print("%s was detected as type %s, but did not meet the PHI detection threashold and will not be redacted." % (phi['Text'], phi['Type']))
            config.not_redacted+=1
    
    print ("Found", len(config.phi_boxes_list), "text boxes to redact.")
    print (config.not_redacted, "additional text boxes were detected, but did not meet the confidence score threshold.")
    return True

