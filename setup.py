#!/usr/bin/env python

from distutils.core import setup

setup(name='watchr',
      version='0.1',
      description='Python version of ruby watchr',
      author='Nathan Landis',
      author_email='my8bird@gmail.com',
      url='https://github.com/my8bird/watchr-py',

      requires = ['watchdog', 'nose'],
      py_modules = ['watchr']
     )
