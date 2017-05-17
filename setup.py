#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'requests'
]

setup(
    name='faces',
    version='0.1.0',
    description="A Python wrapper around FaceApp.",
    long_description=readme + '\n\n' + history,
    author="Vasily Sinitsin",
    author_email='vasilysinitsin@protonmail.com',
    url='https://github.com/vasilysinitsin/faces',
    packages=[
        'faces',
    ],
    package_dir={'faces':
                     'faces'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='faces, faceapp',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
)
