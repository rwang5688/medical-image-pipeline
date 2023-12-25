import config
import os
import image_util
import rekognition_util


def get_env_vars():
    config.profile_name = ''
    config.region_name = os.environ['AWS_REGION']

    # DEBUG
    print("get_env_vars:")
    print("profile_name: %s" % (config.profile_name))
    print("region_name: %s" % (config.region_name))


def lambda_handler(event, context):
    # start
    print('\nStarting de_identify_png.lambda_handler ...')
    print("event: %s" % (event))
    print("context: %s" % (context))

    # get environment variables
    get_env_vars()

    # function parameters
    source_bucket_name = 'medical-images-png-1234567890ab-us-west-2'
    source_prefix = 'data/'
    source_object_name ='image.png'
    config.dpi = 72
    config.phi_detection_threshold = 0.00
    config.redacted_box_color='red'

    # get image from S3 bucket object
    img = image_util.get_image_from_s3_object(source_bucket_name, source_prefix, source_object_name)
    
    # get detected texts from S3 bucket object
    success = rekognition_util.get_detected_texts_from_s3_object(source_bucket_name, source_prefix, source_object_name)
    
    print("text_block: %s" % (config.text_block))
    print("offset_array: %s" % (config.offset_array))
    print("total_length: %d" % (config.total_length))
    print("total_offsets: %d" % (config.total_offsets))

    # end
    print('\n... Thaaat\'s all, Folks!')


if __name__ == '__main__':
    event = {}
    context = {}
    lambda_handler(event, context)

