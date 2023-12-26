import config
import os
import image_util


def get_env_vars():
    # AWS parameters
    config.profile_name = ''
    config.region_name = os.environ['AWS_REGION']

    # DEBUG
    print("get_env_vars:")
    print("profile_name: %s" % (config.profile_name))
    print("region_name: %s" % (config.region_name))


def get_event_vars(event):
    global source_bucket_name
    global source_prefix
    global source_object_name
    global dest_bucket_name
    global dest_prefix
    global dest_object_name

    # function input and output locations (should be from event)
    source_bucket_name = 'medical-images-dcm-1234567890ab-us-west-2'
    source_prefix = 'data/'
    source_object_name ='image.dcm'
    dest_bucket_name = 'medical-images-png-1234567890ab-us-west-2'
    dest_prefix = 'data/'
    dest_object_name = source_object_name.split(".")[-2] + '.png'

    # DEBUG
    print("source_bucket_name: %s" % (source_bucket_name))
    print("source_prefix: %s" % (source_prefix))
    print("source_object_name: %s" % (source_object_name))
    print("dest_bucket_name: %s" % (dest_bucket_name))
    print("dest_prefix: %s" % (dest_prefix))
    print("dest_object_name: %s" % (dest_object_name))


def lambda_handler(event, context):
    # start
    print('\nStarting dcm_to_png.lambda_handler ...')
    print("event: %s" % (event))
    print("context: %s" % (context))

    # get environment variables
    get_env_vars()

    # get event variables
    get_event_vars(event)

    # convert DICOM image from S3 object to image pixel array
    img = image_util.convert_dicom_image_from_s3_object(source_bucket_name, source_prefix, source_object_name)

    # save image pixel array as S3 object in PNG format
    success = image_util.put_image_as_s3_object(img, dest_bucket_name, dest_prefix, dest_object_name)
    if success:
        print("==")
        print("Successfully executed put_image_as_s3_object ...")
        print("==")
    
    # end
    print('\n... Thaaat\'s all, Folks!')


if __name__ == '__main__':
    event = {}
    context = {}
    lambda_handler(event, context)

