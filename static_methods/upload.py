import sys
import time

import filetype
from django.core.files.storage import FileSystemStorage


def upload_img(request, key):
    root_path = sys.path[0]
    user = request.user.id
    if request.method == 'POST' and key in request.FILES:
        data = request.FILES[key]
        try:
            kind = filetype.guess(data)
            salt1 = hash(request.user.id)
            salt2 = str(round(time.time() * 1000))
            fs = FileSystemStorage()
            if kind.mime.lower().startswith('image'):
                filename = fs.save(
                    f"{root_path}/media/{user}/{user}_{salt1}{salt2}.{kind.extension}", data)
                upload_file_url = fs.url(filename)
                return rf"{user}/{user}_{salt1}{salt2}.{kind.extension}"
            else:
                return None
        except Exception:
            pass
