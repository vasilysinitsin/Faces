# -*- coding: utf-8 -*-
#

# Faces - A Python wrapper around FaceApp.
# Copyright © 2017 Vasily Sinitsin
# e-mail: vasilysinitsin@protonmail.com
#
# You should have received a copy of the MIT License
# along with this program.  If not, see <https://opensource.org/licenses/MIT>.

"""
         _               _                    _               _              _        
        /\ \            / /\                /\ \             /\ \           / /\      
       /  \ \          / /  \              /  \ \           /  \ \         / /  \     
      / /\ \ \        / / /\ \            / /\ \ \         / /\ \ \       / / /\ \__  
     / / /\ \_\      / / /\ \ \          / / /\ \ \       / / /\ \_\     / / /\ \___\ 
    / /_/_ \/_/     / / /  \ \ \        / / /  \ \_\     / /_/_ \/_/     \ \ \ \/___/ 
   / /____/\       / / /___/ /\ \      / / /    \/_/    / /____/\         \ \ \       
  / /\____\/      / / /_____/ /\ \    / / /            / /\____\/     _    \ \ \      
 / / /           / /_________/\ \ \  / / /________    / / /______    /_/\__/ / /      
/ / /           / / /_       __\ \_\/ / /_________\  / / /_______\   \ \/___/ /       
\/_/            \_\___\     /____/_/\/____________/  \/__________/    \_____\/        
                                                                                      
"""

__author__ = """Vasily Sinitsin"""
__email__ = 'vasilysinitsin@protonmail.com'
__version__ = '0.1.0'
__license__ = 'MIT'

import random
import string
import json

import requests

BASE_API_URL = 'https://node-03.faceapp.io/api/v2.9/photos'  # Ensure no slash at the end.
BASE_HEADERS = {'User-agent': "FaceApp/3.2.1 (Linux; Android 8.1)"}
DEVICE_ID_LENGTH = 8


class FaceAppImage(object):
    def __init__(self, url=None, file=None, code=None, device_id=None):
        """
        Class is initialized via image url, file or both code and device_id. Expect IllegalArgSet exception if set is
        wrong.
        Initializing with code and device_id may be useful to rebuild class from plain data.
        :param url: direct link to the image.
        :param file: image file.
        :param code: code of already uploaded to FaceApp file.
        :param device_id: device id should match one that was used for uploading.
        """

        self.code = None
        self.device_id = None

        # To be used for debugging
        self._request = None

        if (url or file) and not (url and file) and not (code or device_id):
            device_id = self._generate_device_id()
            headers = self._generate_headers(device_id)

            if file:  # Just to be understandable.
                pass

            elif url:
                file = requests.get(url).content

            post = requests.post(BASE_API_URL, headers=headers, files={'file': file})
            code = post.json().get('code')

            self._request = post

            if not code:
                error = post.headers['X-FaceApp-ErrorCode']
                if error == 'photo_bad_type':
                    raise BadImageType('Bad image provided.')
                elif error == 'photo_no_faces':
                    raise ImageHasNoFaces('No faces on this image.')
                else:
                    raise BaseFacesException(error)

            self.code = code
            self.device_id = device_id

        elif (code and device_id) and not (url or file):
            self.code = code
            self.device_id = device_id

        else:
            raise IllegalArgSet('Wrong args set. Please use either url, file or code and device_id')

    def apply_filter(self, filter_name, cropped=False):
        """
        This method will apply FaceApp filter to uploaded image. You can apply filters multiple times with same class.
        :param filter_name: name of filter to be applied. List can be obtained from .filters property.
        :param cropped: provide True if you want FaceApp to crop image. True will be forced if filter is cropped-only.
        :return: binary of image.
        """
        code = self.code
        device_id = self.device_id
        headers = self._generate_headers(device_id)

        # Forcing cropped option for appropriate filters.
        if filter_name in self._only_cropped:
            cropped = True

        request = requests.get(
            '{0}/{1}/filters/{2}?cropped={3}'.format(BASE_API_URL, code, filter_name, int(cropped)),
            headers=headers)

        error = request.headers.get('X-FaceApp-ErrorCode')
        if error:
            if error == 'bad_filter_id':
                raise BadFilterID('Filter id is bad.')  # FIXME: If bad filter id has space in name it passes anyway.
            else:
                raise BaseFacesException(error)

        return request.content

    @property
    def filters(self):
        """
        :return: list of filter names to use in apply_filter.
        """
        return [face_app_filter['id'] for face_app_filter in self._request.json().get('filters') if
                not face_app_filter['is_paid']]

    def to_json(self):
        """
        This method will dump instance data to json string. Then class can be recreated with from_json class method.
        It is handy when you have uploader-worker application and have to pass data between.
        :return: json string.
        """
        dump_dict = {'code': self.code, 'device_id': self.device_id}
        return json.dumps(dump_dict)

    @classmethod
    def from_json(cls, json_string):
        """
        This class method will rebuild a class.
        :param json_string: obtained from to_json method.
        :return: FaceAppImage instance.
        """
        data_dict = json.loads(json_string)
        code = data_dict['code']
        device_id = data_dict['device_id']
        return cls(code=code, device_id=device_id)

    @staticmethod
    def _generate_device_id():
        """
        This method will generate device id according to DEVICE_ID_LENGTH.
        :return: device id.
        """
        device_id = ''.join(random.choice(string.ascii_letters) for _ in range(DEVICE_ID_LENGTH))
        return device_id

    @staticmethod
    def _generate_headers(device_id):
        """
        This method will compile BASE_HEADERS with provided device id.
        :param device_id: device id.
        :return: headers dict to be handled by requests.
        """
        BASE_HEADERS.update({'X-FaceApp-DeviceID': device_id})
        return BASE_HEADERS

    @property
    def _only_cropped(self):
        """
        :return: list of filters supported only with cropped option.
        """
        return [face_app_filter['id'] for face_app_filter in self._request.json().get('filters') if
                face_app_filter['only_cropped'] and not face_app_filter['is_paid']]

    def __str__(self):
        return 'FaceAppImage#{}'.format(self.code)


class IllegalArgSet(ValueError):
    """
    Expect this when exclusive or none args provided.
    """
    pass


class BaseFacesException(Exception):
    """
    This is a general module exception. It will show error string received from FaceApp.
    """
    pass


class BadImageType(BaseFacesException):
    """
    Expect this when bad file provided or url returns anything except image.
    """
    pass


class ImageHasNoFaces(BaseFacesException):
    """
    Expect this when FaceApp recognize no faces on image.
    """
    pass


class BadFilterID(BaseFacesException):
    """
    Expect this when FaceApp has no such filter.
    """
    pass
