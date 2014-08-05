#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Setup script for Smart Energy Kit.

Additional file-based inclusions can be found in MANIFEST.in.

The distribution archive is created as a source distribution,
http://docs.python.org/2/distutils/sourcedist.html, using

    python setup.py sdist

Installation is performed using

    python setup.py install [--prefix=${LIBRARY_PATH} --exec-prefix=${BIN_PATH]

where the path arguments within the square brackets are optional.
"""

__author__ = 'Daniel Zhang (張道博)'
__copyright__ = 'Copyright (c) 2014, University of Hawaii Smart Energy Project'
__license__ = 'https://raw.githubusercontent.com/Hawaii-Smart-Energy-Project' \
              '/sek/master/BSD-LICENSE.txt'

from distutils.core import setup

setup(name = 'sek', version = '1.0.0',
      description = 'Project indepdent software related to the Hawaii Smart '
                    'Energy Project.',
      long_description = 'TBW',
      author = 'Daniel Zhang (張道博)',
      author_email = 'See https://github.com/dz1111',
      url = 'https://github.com/Hawaii-Smart-Energy-Project/Maui-Smart-Grid',
      license = 'https://raw.githubusercontent.com/Hawaii-Smart-Energy'
                '-Project/sek/master/BSD-LICENSE.txt',
      platforms = 'OS X, Linux',
      package_dir = {'': 'src'},
      packages = ['sek'],

      # Goes in lib.
      py_modules = [
                 'sek/sek_file_util',
                 'sek/sek_logger',
                 'sek/sek_notifier',
                 'sek/sek_python_util'
      ],

      scripts = [
      ])
