import os
import tempfile
import requests
from django.core.files import File


def retrieve_as_file(url):
    try:
        tmp = tempfile.NamedTemporaryFile("wb", delete=True)
        name = os.path.basename(url)
        result = requests.get(url)

        if result.status_code == 200:
            tmp.write(result.content)
            file = File(open(tmp.name, "rb"))
            file.name = name
            return file
        else:
            return None
    except Exception as e:
        return None
