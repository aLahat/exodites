import requests
import hashlib
from hashlib import algorithms_available
def get_checksum_from_picture(picture: bytes, method: str = "md5") -> str:
    """Calculate the checksum of the provided picture, using the desired method.
    Available methods can be fetched using the the algorithms_available function.
    :param picture: picture as bytes
    :param method: hashing method as string (optional, default=md5)
    :return: checksum as string
    """
    h = hashlib.new(method.lower())
    h.update(picture)
    return h.hexdigest()


def save_picture(picture: bytes, file: str = None) -> int:
    """Save a picture to a file.
    The picture must be provided as it content as bytes.
    The filename must be provided as a str with the absolute or relative path where to store it.
    If no filename is provided, a filename will be generated using the MD5 checksum of the picture, with jpeg extension.
    :param picture: picture content as bytes
    :param file: filename as string, relative or absolute path (optional)
    :return: int returned by file.write
    """
    if file is None:
        file = get_checksum_from_picture(picture) + ".jpeg"
    with open(file, "wb") as f:
        return f.write(picture)

def get_online_person(params=None, **kwargs) -> bytes:
    """Get a picture of a fictional person from the ThisPersonDoesNotExist webpage.
    :param params: params dictionary used by requests.get
    :param kwargs: kwargs used by requests.get
    :return: the image as bytes
    """
    r = requests.get("https://thispersondoesnotexist.com/image", headers={'User-Agent': 'My User Agent 1.0'}).content
    return r


def save_online_person(file: str = None, params=None, **kwargs) -> int:
    """Get a picture of a fictional person from the ThisPersonDoesNotExist webpage, and save it to a file.
    The filename must be provided as a str with the absolute or relative path where to store it.
    If no filename is provided, a filename will be generated using the MD5 checksum of the picture, with jpeg extension.
    :param file: filename as string, relative or absolute path (optional)
    :param params: params dictionary used by requests.get
    :param kwargs: kwargs used by requests.get
    :return: int returned by file.write
    """
    picture = get_online_person(params, **kwargs)
    return save_picture(picture, file)




def download(ID):
    f='static/img/'+ID+'.jpeg'
    save_online_person(f)
