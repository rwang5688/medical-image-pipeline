import argparse
import json
import logging
from pprint import pformat

import config
import image_util
import lambda_util


LOGGER = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)


def get_event_vars(event):
    # AWS parameters
    config.profile_name = event['profile_name']
    config.region_name = event['region_name']

    # Data locations
    config.dcm_bucket_name = event['dcm_bucket_name']
    config.dcm_object_prefix = event['dcm_object_prefix']
    config.dcm_object_name = event['dcm_object_name']
    config.png_bucket_name = event['png_bucket_name']
    config.de_id_png_bucket_name = event['de_id_png_bucket_name']
    
    # Pipeline parameters
    config.dpi = event['dpi']
    config.phi_detection_threshold = event['phi_detection_threshold']
    config.redacted_box_color = event['redacted_box_color']

    # DEBUG
    print("get_event_vars:")
    print("profile_name: %s" % (config.profile_name))
    print("region_name: %s" % (config.region_name))
    print("dcm_bucket_name: %s" % (config.dcm_bucket_name))
    print("dcm_object_prefix: %s" % (config.dcm_object_prefix))
    print("dcm_object_name: %s" % (config.dcm_object_name))
    print("png_bucket_name: %s" % (config.png_bucket_name))
    print("de_id_png_bucket_name: %s" % (config.de_id_png_bucket_name))
    print("dpi: %s" % (config.dpi))
    print("phi_detection_threshold: %s" % (config.phi_detection_threshold))
    print("redacted_box_color: %s" % (config.redacted_box_color))


def lambda_handler(event, context):
    # start
    print('\nStarting dcm_to_png.lambda_handler ...')
    LOGGER.info("%s", pformat({"Context" : context, "Request": event}))

    # get event variables
    get_event_vars(event)

    # convert DICOM image from S3 object to image pixel array
    source_bucket_name = config.dcm_bucket_name
    source_object_prefix = config.dcm_object_prefix
    source_object_name = config.dcm_object_name
    img = image_util.convert_dicom_image_from_s3_object(source_bucket_name, source_object_prefix, source_object_name)

    # save image pixel array as S3 object in PNG format
    dest_bucket_name = config.png_bucket_name
    dest_object_prefix = config.dcm_object_prefix
    dest_object_name = config.dcm_object_name.split(".")[-2] + '.png'
    success = image_util.put_image_as_s3_object(img, dest_bucket_name, dest_object_prefix, dest_object_name)

    # async invoke de-identify-png Lambda function
    if success:
        print("==")
        print("Put PNG image as S3 object succeeded.")
        print("Async invoke de-identify-png Lambda function ...")
        source_bucket_name = config.png_bucket_name
        source_object_prefix = config.dcm_object_prefix
        source_object_name = config.dcm_object_name.split(".")[-2] + '.png'
        dest_bucket_name = config.de_id_png_bucket_name
        success = lambda_util.de_identify_png_async(source_bucket_name, source_object_prefix, source_object_name)
        if success:
            print("Async invoke succeeded.")
        else:
            print("Async invoke failed.")
        print("==")
    else:
        print("==")
        print("Put PNG image as S3 object failed.")
        print("Skip async invocation of de-identify-png Lambda function.")
        print("==")
        
    # end
    print('\n... Thaaat\'s all, Folks!')


if __name__ == '__main__':
    # read arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--task-spec", required=True, help="Task specification.")
    args = vars(ap.parse_args())
    print("mip-dcm-to-png: args = %s" % (args))

    # load json file
    task_spec_file_name = args['task_spec']
    f = open(task_spec_file_name)
    event = json.load(f)
    f.close()
    print("mip-dcm-to-png: task_spec = %s" % (event))

    # create test context
    context = {}

    # Execute test
    lambda_handler(event, context)

