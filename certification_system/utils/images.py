import uuid
import os
from django.core.files.storage import default_storage


def get_file_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join("certificates", filename)


def save_temporary_image(file_obj):
    filename = str(uuid.uuid4()) + ".png"
    with default_storage.open(filename, "wb+") as destination:
        for chunk in file_obj.chunks():
            destination.write(chunk)
    import os

    print(os.getcwd())
    return "media/" + filename


def delete_temporary_image(filename):
    default_storage.delete(filename.split("/")[-1])
