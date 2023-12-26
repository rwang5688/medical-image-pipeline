import boto3
from botocore.exceptions import ClientError
import config
import io
import logging
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import os
from PIL import Image


def get_s3_resource():
    print('get_s3_resource: profile_name=%s, region_name=%s' % (config.profile_name, config.region_name))

    p_name = None
    if (config.profile_name != ''):
        p_name = config.profile_name
    session = boto3.Session(profile_name=p_name)
    s3 = session.resource('s3', region_name=config.region_name)
    return s3


def get_image_from_s3_object(source_bucket_name, source_prefix, source_object_name):
    img = None
    
    s3 = get_s3_resource()
    if s3 is None:
        print('get_image_from_s3_object: Failed to get s3 resource.')
        return img
      
    try:
        #Download the image from S3 and hold it in memory
        img_bucket = s3.Bucket(source_bucket_name)
        img_object = img_bucket.Object(source_prefix+source_object_name)
        stream = io.BytesIO()
        img_object.download_fileobj(stream)
    except ClientError as e:
        logging.error("get_image_from_s3_object: unexpected error: ")
        logging.exception(e)
        return img
       
    # Create raw image from stream
    img = np.array(Image.open(stream), dtype=np.uint8)
    # Set the image color map to grayscale, turn off axis graphing
    height, width = img.shape
    # What size does the figure need to be in inches to fit the image?
    figsize = width / float(config.dpi), height / float(config.dpi)
    # Create a figure of the right size with one axes that takes up the full figure
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])
    # Hide spines, ticks, etc.
    ax.axis('off')
    # Render the axis in grayscale
    ax.imshow(img, cmap='gray')

    print('get_image_from_s3_object: Display raw image.')
    plt.show()

    return img


def get_s3_client():
    print('get_s3_client: profile_name=%s, region_name=%s' % (config.profile_name, config.region_name))

    p_name = None
    if (config.profile_name != ''):
        p_name = config.profile_name
    session = boto3.Session(profile_name=p_name)
    s3 = session.client('s3', region_name=config.region_name)
    return s3


def put_image_as_s3_object(image_file_name, dest_bucket_name, dest_prefix, dest_object_name):
    s3 = get_s3_client()
    if s3 is None:
        print('put_image_as_s3_object: Failed to get s3 client.')
        return False
    
    # If S3 object_name was not specified, use inage_file_name
    if dest_object_name is None:
        dest_object_name = os.path.basename(image_file_name)

    # Upload the file
    try:
        response = s3.upload_file(image_file_name, dest_bucket_name, dest_prefix+dest_object_name)
    except ClientError as e:
        logging.error("put_image_as_s3_object: unexpected error: ")
        logging.error(e)
        return False
    
    return True

