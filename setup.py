#!/usr/bin/env python3
# -*- coding: utf-8; tab-width: 4; mode: python -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: t -*
# vi: set ft=python sts=4 ts=4 sw=4 noet 

#    pygifme is a simple command line tool to generate animated GIFs
#    It is a python port from the original ruby script gifme created by
#    Zach Holman

#    Copyright (C) 2013 by Ángel Guzmán Maeso, shakaran at gmail dot com

#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

import sys

if sys.version_info[:3] < (3, 0, 0):
    print('Python 3.0 or higher is required, {0} found. Aborting.'.format('.'.join(map(str, sys.version_info[:3]))))
    sys.exit(1)

print("Python starts at " + sys.prefix)

import platform
print ('Distribution:', ' '.join(map(str, platform.dist())))

__long_description__  = """pygifme is a simple command line tool to generate animated GIFs.
It is a python port from the original ruby script gifme created by Zach Holman"""

__classifiers__       = [
                            'Development Status :: 3 - Alpha',
                            'Environment :: Console',
                            'Environment :: MacOS X',
                            'Environment :: Web Environment',
                            'Intended Audience :: End Users/Desktop',
                            'Intended Audience :: Developers',
                            'Intended Audience :: System Administrators',
                            'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
                            'Natural Language :: English',
                            'Operating System :: POSIX',
                            'Operating System :: POSIX :: Linux',
                            #'Operating System :: Microsoft :: Windows', # Not yet
                            'Operating System :: MacOS',
                            'Operating System :: MacOS :: MacOS X',
                            'Programming Language :: Python',
                            'Programming Language :: Python :: 3',
                            'Programming Language :: Python :: 3.0',
                            'Programming Language :: Python :: 3.1',
                            'Programming Language :: Python :: 3.2',
                            'Programming Language :: Python :: 3.3',
                            'Programming Language :: Python :: Implementation',
                            'Topic :: Multimedia :: Graphics :: Graphics Conversion',
                            'Topic :: Utilities',
                       ]

__data_files__ = [
                  ('/usr/share/doc', ['README.md']),
                 ]

try:
    import os

    from distutils.core import setup
    from distutils.core import Command
    
    from unittest import TestLoader, TextTestRunner
    from doctest import DocTestSuite
    
    # remove MANIFEST. distutils doesn't properly update it when the
    # contents of directories change.
    if os.path.exists('MANIFEST'): 
        os.remove('MANIFEST')
    
    class Test(Command):
        description = 'run unit tests and doc tests'
    
        user_options = []
    
        def initialize_options(self):
            pass
    
        def finalize_options(self):
            pass
    
        def run(self):
            pynames = ['test']
    
            # Add unit-tests:
            loader = TestLoader()
            suite = loader.loadTestsFromNames(pynames)
    
            # Add doc-tests:
            for name in pynames:
                suite.addTest(DocTestSuite(name))
    
            # Run the tests:
            runner = TextTestRunner(verbosity=2)
            result = runner.run(suite)
            if not result.wasSuccessful():
                raise SystemExit(2)
    
    from os.path import join as pjoin
    
    kw = {
          'scripts': [pjoin('bin', 'pygifme'), 'pygifme.py'], 
          'cmdclass' : {
                        'test' : Test, # Test support only for distutils (no setuptools)
                       }
         }
except ImportError:
    from setuptools import setup
    kw = {'entry_points':
          """[console_scripts]\npygifme = pygifme:main\n""",
          'zip_safe': False}

setup(
      name             = 'pygifme',
      version          = '0.1',
      description      = 'pygifme is a simple command line tool to generate animated GIFs.',
      long_description = __long_description__,
      author           = 'Ángel Guzmán Maeso',
      author_email     = 'shakaran@gmail.com',
      maintainer       = 'Ángel Guzmán Maeso',
      maintainer_email = 'shakaran@gmail.com',
      url              = 'https://github.com/shakaran/pygifme',
      download_url     = 'https://github.com/shakaran/pygifme',
      packages         = ['pygifme'],
      package_dir      = {'pygifme': '.'},
      package_data     = {'pygifme': ['setup.py', 'test.py']},
      license          = 'GNU GPL Version 3',
      platforms        = 'Python 3.0 and later',
      classifiers      = __classifiers__,
      keywords         = [],
      data_files       = __data_files__,
      py_modules       = ['pygifme'],
      requires         = ['unitest', 'doctest', 'imagemagick', 'argcomplete'], #cloudapp (ruby) (optional)
      provides         = [],
      obsoletes        = [],
      **kw
)