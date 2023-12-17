import os
from urllib.parse import urlparse
import cloudinary.uploader


class CloudinaryManager:
    """
    A class used to manage image uploads and deletions with Cloudinary.

    ...

    Attributes
    ----------
    folder_name : str
        the name of the folder where images will be uploaded

    Methods
    -------
    upload_image(image_path):
        Uploads an image to Cloudinary.
    delete_image(public_id):
        Deletes an image from Cloudinary.
    rename_image(public_id, new_public_id):
        Renames an image on Cloudinary.
    """

    def __init__(self, folder_name):
        """
        Constructs a new CloudinaryManager instance.

        Parameters
        ----------
        folder_name : str
            the name of the folder where images will be uploaded
        """
        self.folder_name = folder_name

    def upload_image(self, image_path):
        """
        Uploads an image to Cloudinary.

        Parameters
        ----------
        image_path : str
            the path to the image file

        Returns
        -------
        dict
            the response from Cloudinary
        """
        response = cloudinary.uploader.upload(image_path, folder=self.folder_name)
        return response

    def delete_image(self, public_id):
        """
        Deletes an image from Cloudinary.

        Parameters
        ----------
        public_id : str
            the public ID of the image to delete

        Returns
        -------
        dict
            the response from Cloudinary
        """
        response = cloudinary.uploader.destroy(public_id)
        return response

    def rename_image(self, public_id, new_public_id):
        """
        Renames an image on Cloudinary.

        Parameters
        ----------
        public_id : str
            the public ID of the image to rename
        new_public_id : str
            the new public ID for the image

        Returns
        -------
        dict
            the response from Cloudinary
        """
        response = cloudinary.uploader.rename(public_id, new_public_id)
        return response

    def get_transformed_image_url(public_id):
        """
        Returns the URL of an image on Cloudinary with transformations applied.

        Parameters
        ----------
        public_id : str
            the public ID of the image

        Returns
        -------
        str
            the URL of the transformed image
        """
        url = cloudinary.url(
            public_id,
            transformation=[
                {"width": 500, "height": 500, "crop": "fill"},
                {"effect": "sepia"},
            ],
        )

        return url

    def get_public_id(self,url):
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
