#!/usr/bin/python
# coding: utf-8

import unittest

import faces


class FacesTest(unittest.TestCase):
    def setUp(self):
        self.valid_image = open('Roosevelt.jpg', 'rb')
        self.valid_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/President_Roosevelt_-_Pach_Bros.tif/lossy-page1-220px-President_Roosevelt_-_Pach_Bros.tif.jpg'

        self.image_by_file = faces.FaceAppImage(file=self.valid_image)
        self.image_by_url = faces.FaceAppImage(url=self.valid_url)

    def badFileTest(self):
        bad_file = self.valid_image.read(1)  # Reading just one byte to get invalid image.
        image = faces.FaceAppImage(file=bad_file)

        self.assertRaises(faces.BadImageType)

    def notImageURLTest(self):
        not_image_url = 'https://wikipedia.org'
        image = faces.FaceAppImage(url=not_image_url)

        self.assertRaises(faces.BadImageType)

    def noFacesTest(self):
        no_faces_image = open('Enigma.jpg', 'rb')
        image = faces.FaceAppImage(no_faces_image)

        self.assertRaises(faces.ImageHasNoFaces)

    def filterTest(self):
        self.image_by_file.apply_filter('smile')

    def badFilterTest(self):
        self.image_by_file.apply_filter('Make me as cool as Vasily')

        self.assertRaises(faces.BadFilterID)


if __name__ == "__main__":
    unittest.main()
