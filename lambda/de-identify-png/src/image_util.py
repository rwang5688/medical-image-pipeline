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
    s3 = get_s3_resource()
    if s3 is None:
        print('get_image_from_s3_object: Failed to get s3 resource.')
        return None
    
    img_bucket = None
    img_object = None
    try:
        # Download the PNG image from S3 and hold it in memory as byte stream
        img_bucket = s3.Bucket(source_bucket_name)
        img_object = img_bucket.Object(source_prefix+source_object_name)
        stream = io.BytesIO()
        img_object.download_fileobj(stream)
    except ClientError as e:
        logging.error("get_image_from_s3_object: unexpected error: ")
        logging.exception(e)
        return None
        
    # Create raw image from stream
    img = np.array(Image.open(stream), dtype=np.uint8)

    # Display raw image in grayscale
    height, width = img.shape
    # What size does the figure need to be in inches to fit the image?
    figsize = width / float(config.dpi), height / float(config.dpi)
    # Create a figure of the right size with one axes that takes up the full figure
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])
    # Render image in gray scale
    ax.imshow(img, cmap='gray')

    # Ensure that no axis or whitespaces is printed in the image file we want to display.
    plt.axis('off')
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())

    print('[DEBUG] get_image_from_s3_object: Display raw image.')
    plt.show()

    return img


def redact_and_put_image_as_s3_object(img, dest_bucket_name, dest_prefix, dest_object_name):
    if img is None:
        print('put_image_as_s3_object: Image is null object.')
        return False
    
    s3 = get_s3_resource()
    if s3 is None:
        print('put_image_as_s3_object: Failed to get s3 resource.')
        return False
    
    img_bucket = None
    try:
        # Get dest bucket resource
        img_bucket = s3.Bucket(dest_bucket_name)
    except ClientError as e:
        logging.error("put_image_as_s3_object: unexpected error: ")
        logging.exception(e)
        return False
    
    # Now we use the list of bounding boxes to display de-id image with redacted text boxes.
    height, width = img.shape
    # What size does the figure need to be in inches to fit the image?
    figsize = width / float(config.dpi), height / float(config.dpi)
    # Create a figure of the right size with one axes that takes up the full figure
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0, 0, 1, 1])
    # Render image in gray scale
    ax.imshow(img, cmap='gray')
    # Render redacted text boxes
    for box in config.phi_boxes_list:
        #The bounding boxes are described as a ratio of the overall image dimensions, so we must multiply them
        #by the total image dimensions to get the exact pixel values for each dimension.
        x = img.shape[1] * box['Left']
        y = img.shape[0] * box['Top']
        width = img.shape[1] * box['Width']
        height = img.shape[0] * box['Height']
        rect = patches.Rectangle((x,y),width,height,linewidth=0,edgecolor=config.redacted_box_color,facecolor=config.redacted_box_color)
        ax.add_patch(rect)

    # Ensure that no axis or whitespaces is printed in the image file we want to display (and save).
    plt.axis('off')
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())

    # Must call pyplot.savefig() before pyplot.show().
    # Save de-id image with redacted text boxes to a byte stream in PNG format.
    # Rewind the byte stream and put to the dest bucket as dest_prefix+dest_object_name.
    img_data = io.BytesIO()
    plt.savefig(img_data, bbox_inches='tight', pad_inches=0, format='png')
    img_data.seek(0)
    img_bucket.put_object(Body=img_data, ContentType='image/png', Key=dest_prefix+dest_object_name)

    print('[DEBUG] put_image_as_s3_object: Display de-id image with redacted text boxes.')
    plt.show()

    return True

