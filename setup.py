# -*- coding: utf-8 -*-
# setup

__author__ = "Paul K. Korir, PhD"
__email__ = "paul.korir@gmail.com"
__date__ = "2017-06-02"

import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    long_description = f.read()
    
setup(
    name="python-units",
    version="0.1.2.post0",
    author="Paul K. Korir, PhD",
    author_email = "paul.korir@gmail.com",
    url="https://bacculus.dev/paulkorir/units",
    description="Python library to represent numbers with units",
    long_description=long_description,
    license="GNU GPL v3.0",
    keywords="units",
    )
