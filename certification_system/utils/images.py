import uuid
import os
from django.core.files.storage import default_storage
from pathlib import Path


def get_file_path(instance, filename):
    """This function is used to get the file path for the uploaded file

    Args:
        instance (ModelInstance): Django model instance
        filename (_type_): Name of the file to be saved

    Returns:
        _type_: returns the path of the file, where it is to be saved
    """

    ext = filename.split(".")[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join("certificates", filename)


def save_temporary_image(file_obj):
    """Saves django image in the media folder

    Args:
        file_obj (InMemoryImage): In memory image object

    Returns:
        str: Path of the image from the directory containing manage.py
    """
    filename = str(uuid.uuid4()) + ".png"
    with default_storage.open(filename, "wb+") as destination:
        for chunk in file_obj.chunks():
            destination.write(chunk)

    return Path("media") / filename


def delete_temporary_image(filepath):
    """delete image saved by save_temporary_image

    Args:
        filename (str): Path of the image calculated from the directory containing manage.py
    """
    filename = os.path.basename(os.path.normpath(filepath))
    default_storage.delete(filename)
