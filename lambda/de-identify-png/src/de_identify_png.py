import boto3
import io
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os
from PIL import Image


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
    print('\nStarting de_identify_png.lambda_handler ...')
    print("event: %s" % (event))
    print("context: %s" % (context))

    # get environment variables
    get_env_vars()

    # input parameters
    bucket='aws-ml-blog'
    object='artifacts/de-id-medical-images/test.png'
    redacted_box_color='red'
    dpi = 72
    phi_detection_threshold = 0.00

    # open image and read into unsigned int pixel array
    img = np.array(Image.open('../data/image.png'), dtype=np.uint8)

    #Set the image color map to grayscale, turn off axis graphing, and display the image
    height, width = img.shape
    # What size does the figure need to be in inches to fit the image?
    figsize = width / float(dpi), height / float(dpi)
    # Create a figure of the right size with one axes that takes up the full figure
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])
    # Hide spines, ticks, etc.
    ax.axis('off')
    # Display the image.
    ax.imshow(img, cmap='gray')
    plt.show()

    # end
    print('\n... Thaaat\'s all, Folks!')


if __name__ == '__main__':
    event = {}
    context = {}
    lambda_handler(event, context)

