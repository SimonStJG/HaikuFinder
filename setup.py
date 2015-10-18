#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='haiku-finder',
    version='0.1',
    description='Haiku Finder',
    author='Simon StJG',
    author_email='Simon.StJG@gmail.com',
    # url='http://www.SimonStJG.org/',
    packages=['haikufinder'],
    install_requires=['nltk', 'cached_property']
    )
