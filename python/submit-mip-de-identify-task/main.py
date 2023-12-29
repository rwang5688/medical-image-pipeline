import logging
from pprint import pformat

import config
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
    print('\nStarting submit_mip_de_identify_task.lambda_handler ...')
    LOGGER.info("%s", pformat({"Context" : context, "Request": event}))

    # get event variables
    get_event_vars(event)

    # **TO-DO**: get list of ddcm_object_keys based on patient id
    dcm_object_keys =[]
    dcm_object_keys.append(config.dcm_object_prefix+config.dcm_object_name)

    # foreach dcm object, async invoke de-identify-png Lambda function
    for dcm_object_key in dcm_object_keys:
        # this is going to be a little bit tricky since we can't just split on "/"
        # dcm_object_prefix: for everything that to the left of [-1], join on "/".
        # dcm_object_name: [-1]
        dcm_object_prefix = config.dcm_object_prefix
        dcm_object_name = config.dcm_object_name

        # **TO DO**: Parse dcm_object
        source_bucket_name = config.dcm_bucket_name
        source_object_prefix = dcm_object_prefix
        source_object_name = dcm_object_name
        success = lambda_util.dcm_to_png_async(source_bucket_name, source_object_prefix, source_object_name)
        if success:
            print("Async invoke succeeded.")
        else:
            print("Async invoke failed.")
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
    event['dpi'] = '72'
    event['phi_detection_threshold'] = '0.00'
    event['redacted_box_color'] = 'red'
    # create test context
    context = {}
    # Execute test
    lambda_handler(event, context)

