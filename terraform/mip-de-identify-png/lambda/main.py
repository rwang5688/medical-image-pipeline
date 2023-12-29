import logging
from pprint import pformat

import config
import image_util
import rekognition_util
import comprehend_medical_util


LOGGER = logging.getLogger(__name__)
logging.getLogger().setLevel(logging.INFO)


def get_event_vars(event):
    # AWS parameters
    config.profile_name = event['profile_name']
    config.region_name = event['region_name']

    # Data locations
    config.png_bucket_name = event['png_bucket_name']
    config.png_object_prefix = event['png_object_prefix']
    config.png_object_name = event['png_object_name']
    config.de_id_png_bucket_name = event['de_id_png_bucket_name']

    # Pipeline parameters
    config.dpi = int(event['dpi'])
    config.phi_detection_threshold = float(event['phi_detection_threshold'])
    config.redacted_box_color = event['redacted_box_color']

    # DEBUG
    print("get_env_vars:")
    print("profile_name: %s" % (config.profile_name))
    print("region_name: %s" % (config.region_name))
    print("png_bucket_name: %s" % (config.png_bucket_name))
    print("png_object_prefix: %s" % (config.png_object_prefix))
    print("png_object_name: %s" % (config.png_object_name))
    print("de_id_png_bucket_name: %s" % (config.de_id_png_bucket_name))
    print("dpi: %d" % (config.dpi))
    print("phi_detection_threshold: %f" % (config.phi_detection_threshold))
    print("redacted_box_color: %s" % (config.redacted_box_color))


def lambda_handler(event, context):
    # start
    print('\nStarting de_identify_png.lambda_handler ...')
    LOGGER.info("%s", pformat({"Context" : context, "Request": event}))

    # get event variables
    get_event_vars(event)

    # get detected texts and offsets from S3 bucket object
    source_bucket_name = config.png_bucket_name
    source_object_prefix = config.png_object_prefix
    source_object_name = config.png_object_name
    success = rekognition_util.get_detected_texts_from_s3_object(source_bucket_name, source_object_prefix, source_object_name)
    if success:
        print("==")
        print("Successfully executed get_detect_texts_from_s3_object ...")
        print("detected_texts_list: %s" % (config.detected_texts_list))
        print("text_block: %s" % (config.text_block))
        print("total_length: %d" % (config.total_length))
        print("offset_array: %s" % (config.offset_array))
        print("total_offsets: %d" % (config.total_offsets))
        print("==")

    # get detected PHIs and bounding boxes from detected texts
    success = comprehend_medical_util.get_phi_boxes_list_from_detected_texts()
    if success:
        print("==")
        print("Successfully executed get_phi_boxes_list_from_detected_texts ...")
        print("detected_phi_list: %s" % (config.detected_phi_list))
        print("phi_scores_list: %s" % (config.phi_scores_list))
        print("phi_texts_list: %s" % (config.phi_texts_list))
        print("phi_types_list: %s" % (config.phi_types_list))
        print("phi_boxes_list: %s" % (config.phi_boxes_list))
        print("not_redacted: %d" % (config.not_redacted))
        print("==")

    # get image pixel array from S3 object
    source_bucket_name = config.png_bucket_name
    source_object_prefix = config.png_object_prefix
    source_object_name = config.png_object_name
    img = image_util.get_image_from_s3_object(source_bucket_name, source_object_prefix, source_object_name)

    # redact and put image pixel array as S3 object in PNG format
    dest_bucket_name = config.de_id_png_bucket_name
    dest_object_prefix = config.png_object_prefix
    dest_object_name ='de-id-'+ config.png_object_name
    success = image_util.redact_and_put_image_as_s3_object(img, dest_bucket_name, dest_object_prefix, dest_object_name)
    if success:
        print("==")
        print("Successfully executed redact_and_put_image_as_s3_object ...")
        print("==")
    
    # end
    print('\n... Thaaat\'s all, Folks!')


if __name__ == '__main__':
    # Create test event
    event = {}
    event['profile_name'] = ''
    event['region_name'] = 'us-west-2'
    event['png_bucket_name'] = 'medical-images-png-1234567890ab-us-west-2'
    event['png_object_prefix'] = 'test/'
    event['png_object_name'] = 'image.png'
    event['de_id_png_bucket_name'] = 'medical-images-de-id-png-1234567890ab-us-west-2'
    event['dpi'] = '72'
    event['phi_detection_threshold'] = '0.00'
    event['redacted_box_color'] = 'red'
    # create test context
    context = {}
    # This is a test
    config.is_test = True
    # Execute test
    lambda_handler(event, context)
