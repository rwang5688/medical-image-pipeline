import logging
from pprint import pformat

import config
import image_util


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

    # DEBUG
    print("get_env_vars:")
    print("profile_name: %s" % (config.profile_name))
    print("region_name: %s" % (config.region_name))
    print("dcm_bucket_name: %s" % (config.dcm_bucket_name))
    print("dcm_object_prefix: %s" % (config.dcm_object_prefix))
    print("dcm_object_name: %s" % (config.dcm_object_name))
    print("png_bucket_name: %s" % (config.png_bucket_name))
    print("de_id_png_bucket_name: %s" % (config.de_id_png_bucket_name))


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
    if success:
        print("==")
        print("Successfully executed put_image_as_s3_object ...")
        print("==")

    # async invoke de-identify-png Lambda function
    if config.is_test:
        print("==")
        print("Testing mode: Skip invoking de-identify-png Lambda function")
        print("==")
    else:
        print("==")
        print("**TO-DO**: Async invoke de-identify-png Lambda function.")
        print("==")

    # end
    print('\n... Thaaat\'s all, Folks!')


if __name__ == '__main__':
    # Create test event
    event = {}
    event['profile_name'] = ''
    event['region_name'] = 'us-west-2'
    event['dcm_bucket_name'] = 'medical-images-dcm-1234567890ab-us-west-2'
    event['dcm_object_prefix'] = 'test/'
    event['dcm_object_name'] = 'image.dcm'
    event['png_bucket_name'] = 'medical-images-png-1234567890ab-us-west-2'
    event['de_id_png_bucket_name'] = 'medical-images-de-id-png-1234567890ab-us-west-2'
    # create test context
    context = {}
    # This is a test
    config.is_test = True
    # Execute test
    lambda_handler(event, context)

