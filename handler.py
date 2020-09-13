import io
from typing import Optional, Any, Union
from urllib.request import urlopen

import boto3
import numpy as np
from PIL import Image
from skimage import feature


def handle(event, context):
    # aws test event (internal use, at least)
    if url := _get_nested(event, 'image_url'):
        with urlopen(url) as conn:
            image_in = Image.open(conn)
        key = url
    # aws s3 create event
    elif s3_event := _get_nested(event, 'Records', 0, 's3'):
        key, image_in = _handle_s3(s3_event)
    # unhandled event
    else:
        raise ValueError(f'malformed event: {event}')
    image_out = _process_image(image_in)
    _s3_upload(image_out, 'workshop-aws-output', key)


def _handle_s3(s3_event: dict):
    bucket_name = _get_nested(s3_event, 'bucket', 'name')
    object_key = _get_nested(s3_event, 'object', 'key')
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    s3_object = bucket.Object(object_key)
    buffer = io.BytesIO()
    s3_object.download_fileobj(buffer)
    return object_key, Image.open(buffer)


def _s3_upload(image: Image, bucket_name: str, object_key: str):
    buffer = io.BytesIO()
    image.save(buffer, format=image.format)
    buffer.seek(0)
    s3 = boto3.client('s3')
    s3.upload_fileobj(buffer, bucket_name, object_key)


def _process_image(image_in: Image) -> Image:
    grayscale_data = np.array(image_in.convert('L'))
    edges = feature.canny(grayscale_data, sigma=3)
    image_out = Image.fromarray(edges)
    image_out.format = image_in.format
    return image_out


def _get_nested(obj: dict, *path: Union[str, int]) -> Optional[Any]:
    key = path[0]
    if isinstance(key, int):
        if len(obj) <= key:
            val = None
        else:
            val = obj[key]
    else:
        val = obj.get(key, None)
    if val is not None and len(path) > 1:
        return _get_nested(val, *path[1:])
    return val
