import boto3
from botocore.exceptions import ClientError
import json
import logging

import config


def get_lambda_client():
    print('get_lambda_client: profile_name=%s, region_name=%s' % (config.profile_name, config.region_name))

    p_name = None
    if (config.profile_name != ''):
        p_name = config.profile_name
    session = boto3.Session(profile_name=p_name)
    lmb = session.client('lambda', region_name=config.region_name)
    return lmb
    

def de_identify_png_async(source_bucket_name, source_object_prefix, source_object_name):
    lmb = get_lambda_client()
    if lmb is None:
        print('de_identify_png_async: Failed to get lambda client.')
        return False
        
    try:
        payload = {}
        payload["profile_name"] = config.profile_name
        payload["region_name"] = config.region_name
        payload["png_bucket_name"] = source_bucket_name
        payload["png_object_prefix"] = source_object_prefix
        payload["png_object_name"] = source_object_name
        payload["de_id_png_bucket_name"] = config.de_id_png_bucket_name
        payload["dpi"] = config.dpi
        payload["phi_detection_threshold"] = config.phi_detection_threshold
        payload["redacted_box_color"] = config.redacted_box_color
        print("de_identify_png_async: Invoke mip-de-identify-png with payload({})".format(payload))
        
        status = lmb.invoke(
                FunctionName='mip-de-identify-png',
                InvocationType='Event',
                Payload=json.dumps(payload),
                )
    except ClientError as e:
        logging.error("de_identify_png_async: unexpected error: ")
        logging.exception(e)
        return False

    return True
    
    