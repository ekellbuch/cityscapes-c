#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

from glob import glob
from os.path import basename
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


setup(
    name="template",
    version="0.0.0",
    description="Template 1",
    author="Author",
    author_email="email",
    url="url",
    #packages=find_packages('src/deepgraphpose'),
    packages=['template'],
    package_dir={'':'src/template'},
    #py_modules=[
    #    splitext(basename(path))[0]
    #    for path in glob("src/deepgraphpose/graphpose/*.py", recursive=True)
    #],
    include_package_data=True,
    zip_safe=False, #install_requires=['numpy', 'matplotlib']
)
