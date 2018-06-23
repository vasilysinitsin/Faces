#!/usr/bin/python
# coding: utf-8

import unittest

import faces


class FacesTest(unittest.TestCase):
    def setUp(self):
        with open('tests/Roosevelt.jpg', 'rb') as valid_image:
            self.image_by_file = faces.FaceAppImage(file=valid_image)

        valid_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/President_Roosevelt_-_Pach_Bros.tif/lossy-page1-220px-President_Roosevelt_-_Pach_Bros.tif.jpg'
        self.image_by_url = faces.FaceAppImage(url=valid_url)

    def testBadFile(self):
        with self.assertRaises(faces.BadImageType):
            with open('.travis.yml', 'rb') as bad_file:
                image = faces.FaceAppImage(file=bad_file)

    def testNotImage(self):
        with self.assertRaises(faces.BadImageType):
            not_image_url = 'https://wikipedia.org'
            image = faces.FaceAppImage(url=not_image_url)

    def testNoFaces(self):
        with self.assertRaises(faces.ImageHasNoFaces):
            with open('tests/Enigma.jpg', 'rb') as no_faces_image:
                image = faces.FaceAppImage(file=no_faces_image)

    def testFilter(self):
        self.image_by_file.apply_filter('smile')

    def testBadFilter(self):
        with self.assertRaises(faces.BadFilterID):
            self.image_by_file.apply_filter('Make_me_as_cool_as_Vasily')


class TestKnownFilters(unittest.TestCase):
    def setUp(self):
        with open('tests/Roosevelt.jpg', 'rb') as valid_image:
            self.image_by_file = faces.FaceAppImage(file=valid_image)

    def testFilterSet(self):
        """
        This test has print() output and is used to check if known filters are not deprecated or removed from API.
        Overall test will only fail if none of known filters works. Otherwise it seems to be an API problem.
        """
        print('\nFilters probe...')
        for num, face_app_filter in enumerate(self.image_by_file.filters):
            try:
                self.image_by_file.apply_filter(face_app_filter)
                status = 'OK'
            except faces.BadFilterID:
                status = 'FAIL'
            print('Probed filter "{}" : {}'.format(face_app_filter, status))
        print('DONE. {} filters operational.'.format(num))
        if not num:
            raise Exception('All known filters failed.')


if __name__ == "__main__":
    unittest.main()
