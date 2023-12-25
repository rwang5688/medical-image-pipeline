import boto3
import numpy as np
import os
from PIL import Image
import pydicom


def get_env_vars():
    global profile_name
    global region_name

    profile_name = ''
    region_name = os.environ['AWS_REGION']

    # DEBUG
    print("get_env_vars:")
    print("profile_name: %s" % (profile_name))
    print("region_name: %s" % (region_name))


def lambda_handler(event, context):
    # start
    print('\nStarting dcm_to_png.lambda_handler ...')
    print("event: %s" % (event))
    print("context: %s" % (context))

    # get environment variables
    get_env_vars()

    # read DCM file into float pixel array
    ds = pydicom.dcmread('../input/image.dcm')
    new_image = ds.pixel_array.astype(float)

    # scale the image in pixel array
    scaled_image = (np.maximum(new_image, 0) / new_image.max()) * 255.0

    # convert to unsigned int pixel array
    scaled_image = np.uint8(scaled_image)

    # extract image from unsigned int pixel array
    final_image = Image.fromarray(scaled_image)

    # DEBUG: display image
    final_image.show()

    # save image as JPG and PNG files
    final_image.save('../output/image.jpg')
    final_image.save('../output/image.png')

    # end
    print('\n... Thaaat\'s all, Folks!')


if __name__ == '__main__':
    event = {}
    context = {}
    lambda_handler(event, context)

