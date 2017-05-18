# Faces
# :pensive: →  :grinning:

A Python wrapper around [FaceApp](https://www.faceapp.com/) .

## Installation
`$ pip install git+https://github.com/vasilysinitsin/Faces.git`
or manually clone this repo.
 
## Basic Usage
### With file,
```python
import faces

sad = open('sad.jpg', 'rb')
image = faces.FaceAppImage(file=sad)
happy = image.apply_filter('smile', cropped=True)
```
### with URL
```python
import faces

old_rockfeller = 'https://upload.wikimedia.org/wikipedia/commons/6/6f/John_D._Rockefeller_1885.jpg'
image = faces.FaceAppImage(url=old_rockfeller)
young_rockfeller = image.apply_filter('young')
```
### or with FaceApp code and device id
```python
import faces

code_of_me_uploaded = '20170517181457gflf'
my_device_id = '12345678'
image = faces.FaceAppImage(code=code_of_me_uploaded, device_id=my_device_id)
brad_pitt = image.apply_filter('hot')
```

## Handling Exceptions
```python
try:
image = faces.FaceAppImage(...)
except faces.ImageHasNoFaces:
    print('Your face is not recognized. Are you an alian?')
except faces.BaseFacesException:
    print('Some unknown wrong things happened.')
try:
    result = image.apply_filter('young, rich and powerful')
except faces.BadFilterID:
    print('Too cool filter to exist.')
```

## Known filters
Try that ones: `smile`, `smile_2`, `hot`, `old`, `young`, `female`, `male`.

## Advanced features
### Dumping and rebuilding class from json
```python
# It is handy when you have uploader-worker application and have to pass data between.

image = faces.FaceAppImage(...)
json_string = image.to_json() # type(json_string) == str

"""
...pass to different machine
"""

rebuilt_image = faces.FaceAppImage.from_json(json_string) # type(rebuilt_image) == faces.FaceAppImage
```

## Yes, it's that easy. Now create something cool!