import boto3
from botocore.exceptions import ClientError
import config
import io
import logging
import numpy as np
import os
from PIL import Image
import pydicom


def get_s3_client():
    print('get_s3_client: profile_name=%s, region_name=%s' % (config.profile_name, config.region_name))

    p_name = None
    if (config.profile_name != ''):
        p_name = config.profile_name
    session = boto3.Session(profile_name=p_name)
    s3 = session.client('s3', region_name=config.region_name)
    return s3


def convert_dicom_image_from_s3_object(source_bucket_name, source_prefix, source_object_name):    
    s3 = get_s3_client()
    if s3 is None:
        print('convert_dicom_image_from_s3_object: Failed to get s3 client.')
        return None
    
    try:
        # download the DCM image from S3 as a local file
        with open(source_object_name, 'wb') as data:
            s3.download_fileobj(source_bucket_name, source_prefix+source_object_name, data)
    except ClientError as e:
        logging.error("convert_dicom_image_from_s3_object: unexpected error: ")
        logging.exception(e)
        return None
    
    # read DCM file into float pixel array
    ds = pydicom.dcmread(source_object_name)
    new_image = ds.pixel_array.astype(float)

    # scale the image in pixel array
    scaled_image = (np.maximum(new_image, 0) / new_image.max()) * 255.0

    # convert to unsigned int pixel array
    scaled_image = np.uint8(scaled_image)

    # extract image from unsigned int pixel array
    img = Image.fromarray(scaled_image)

    # DEBUG: Display image
    print("[DEBUG] convert_dicom_image_from_s3_object: Display converted image.")
    img.show()

    return img


def put_image_as_s3_object(img, dest_bucket_name, dest_prefix, dest_object_name):
    if img is None:
        print('put_image_as_s3_object: Image is null object.')
        return False
    
    s3 = get_s3_client()
    if s3 is None:
        print('put_image_as_s3_object: Failed to get s3 resource.')
        return False
    
    img_bucket = None
    try:
        # save image as local PNG file
        img.save(dest_object_name)
        # upload load PNG file to S3
        response = s3.upload_file(dest_object_name, dest_bucket_name, dest_prefix+dest_object_name)
    except ClientError as e:
        logging.error("put_image_as_s3_object: unexpected error: ")
        logging.exception(e)
        return False
    
    return True

