from django import template
import cloudinary
import os
from urllib.parse import urlparse


register = template.Library()


@register.simple_tag
def transform_image(url):
    """
    Transforms the given image URL using Cloudinary.

    Args:
        url (str): The URL of the image.
        width (int): The desired width of the transformed image.
        height (int): The desired height of the transformed image.
        crop (str, optional): The cropping mode for the transformed image. Defaults to "fill".

    Returns:
        str: The transformed URL of the image.
    """

    # Extract the public ID from the URL
    # parsed_url = urlparse(url)
    # public_id = os.path.splitext(parsed_url.path.lstrip('/'))[0]
    public_id = get_public_id(url)
    print(public_id)
    # Generate the transformed URL
    transformed_url = cloudinary.CloudinaryImage(public_id).build_url(
        transformation=[
            {"width": 200, "crop": "thumb", "gravity": "face", "x": 423, "y": 338}
        ],
        format="webp",
    )
    print(transformed_url)

    return transformed_url


# a template tag to display product detail image using cloudinary and transforming it to be 600x400 with gravity auto crop fill and format webp
@register.simple_tag
def product_detail_image(url):
    """
    Transforms the given image URL using Cloudinary.

    Args:
        url (str): The URL of the image.
        width (int): The desired width of the transformed image.
        height (int): The desired height of the transformed image.
        crop (str, optional): The cropping mode for the transformed image. Defaults to "fill".

    Returns:
        str: The transformed URL of the image.
    """

    # Extract the public ID from the URL
    # parsed_url = urlparse(url)
    # public_id = os.path.splitext(parsed_url.path.lstrip('/'))[0]
    public_id = get_public_id(url)
    print(public_id)
    # Generate the transformed URL
    transformed_url = cloudinary.CloudinaryImage(public_id).build_url(
        transformation=[
            {"width": 600, "height": 400, "crop": "fill", "gravity": "auto"},
        ],
        format="webp",
    )

    return transformed_url


def get_public_id(url):
    """
    Extracts the public ID from a Cloudinary URL.

    Args:
        url (str): The Cloudinary URL.

    Returns:
        str: The public ID extracted from the URL.
    """
    # Parse the URL
    parsed_url = urlparse(url)

    # Split the path into parts
    path_parts = parsed_url.path.split("/")

    # The public ID starts after the version number, which is the part after 'upload' in this case
    upload_index = path_parts.index("upload") + 2

    # Join the parts from the upload index onwards, and remove the file extension
    public_id = os.path.splitext("/".join(path_parts[upload_index:]))[0]

    return public_id


"""
usage example:
{% load cloudinary_tags %}
{% transform_image "https://res.cloudinary.com/dh41vh9dx/image/upload/v1625794192/Shop/Products/1.jpg" 500 500 %}

{% load cloudinary_tags %}
<img src="{% transform_image image_url 300 300 'fill' %}" alt="Image">

modified url example:
 http://res.cloudinary.com/drjerwkgo/image/upload/c_fill,h_300,w_300/v1/drjerwkgo/image/upload/v1692981305/cld-sample-5.webp
http://res.cloudinary.com/drjerwkgo/image/upload/c_fill,g_auto,h_300,w_300/v1/drjerwkgo/image/upload/v1692981305/cld-sample-5.webp
  cloudinary image url example:
 https://res.cloudinary.com/drjerwkgo/image/upload/c_fill,f_webp,h_300,w_300/v1692981305/cld-sample-5.jpg
"""
