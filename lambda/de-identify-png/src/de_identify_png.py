import config
import os
import image_util
import rekognition_util
import comprehend_medical_util


def get_env_vars():
    # AWS parameters
    config.profile_name = ''
    config.region_name = os.environ['AWS_REGION']

    # Pipeline parameters    
    config.dpi = int(os.environ['DPI'])
    config.phi_detection_threshold = float(os.environ['PHI_DETECTION_THRESHOLD'])
    config.redacted_box_color = os.environ['REDACTED_BOX_COLOR']

    # DEBUG
    print("get_env_vars:")
    print("profile_name: %s" % (config.profile_name))
    print("region_name: %s" % (config.region_name))
    print("dpi: %d" % (config.dpi))
    print("phi_detection_threshold: %f" % (config.phi_detection_threshold))
    print("redacted_box_color: %s" % (config.redacted_box_color))


def get_event_vars(event):
    global source_bucket_name
    global source_prefix
    global source_object_name
    global dest_bucket_name
    global dest_prefix
    global dest_object_name

    # function input and output locations (should be from event)
    source_bucket_name = 'medical-images-png-1234567890ab-us-west-2'
    source_prefix = 'data/'
    source_object_name ='image.png'
    dest_bucket_name = 'medical-images-de-id-png-1234567890ab-us-west-2'
    dest_prefix = 'data/'
    dest_object_name ='de-id-'+source_object_name

    # DEBUG
    print("source_bucket_name: %s" % (source_bucket_name))
    print("source_prefix: %s" % (source_prefix))
    print("source_object_name: %s" % (source_object_name))
    print("dest_bucket_name: %s" % (dest_bucket_name))
    print("dest_prefix: %s" % (dest_prefix))
    print("dest_object_name: %s" % (dest_object_name))


def lambda_handler(event, context):
    # start
    print('\nStarting de_identify_png.lambda_handler ...')
    print("event: %s" % (event))
    print("context: %s" % (context))

    # get environment variables
    get_env_vars()
         
    # get event variables
    get_event_vars(event)

    # get detected texts and offsets from S3 bucket object
    success = rekognition_util.get_detected_texts_from_s3_object(source_bucket_name, source_prefix, source_object_name)
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
    img = image_util.get_image_from_s3_object(source_bucket_name, source_prefix, source_object_name)

    # redact and put image pixel array as S3 object in PNG format
    success = image_util.redact_and_put_image_as_s3_object(img, dest_bucket_name, dest_prefix, dest_object_name)
    if success:
        print("==")
        print("Successfully executed redact_and_put_image_as_s3_object ...")
        print("==")
    
    # end
    print('\n... Thaaat\'s all, Folks!')


if __name__ == '__main__':
    event = {}
    context = {}
    lambda_handler(event, context)

