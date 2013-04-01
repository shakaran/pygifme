# -*- coding: utf-8; tab-width: 4; mode: python -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: t -*-
# vi: set ft=python sts=4 ts=4 sw=4 noet 

#    pygifme is a simple command line tool to generate animated GIFs. 
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
from os import system, environ, EX_OK
from subprocess import check_output, CalledProcessError, STDOUT
import unittest

if sys.version_info[:3] < (3, 0, 0):
    print('Python 3.0 or higher is required, {0} found. Aborting.'.format('.'.join(map(str, sys.version_info[:3]))))
    sys.exit(1)

def disable_cloud_app():
    environ['DISABLE_CLOUPAPP'] = '1'
    
def enable_cloud_app():
    if environ.get('DISABLE_CLOUPAPP'):
        del environ['DISABLE_CLOUPAPP']

class TestBinaries(unittest.TestCase):
    """ Test Binaries """
        
    @unittest.skipIf(sys.version_info < (2, 6),
                     'argparse not supported in this python version')
    def test_argpase(self):
        """ Checks the presence of argparse module """
        try:
            import argparse
            assert True
        except ImportError as e:
            self.fail('The module argparse is required')
       
    def test_argcomplete(self):
        """ Checks the presence of argcomplete module """
        try:
            import argcomplete
            assert True
        except ImportError as e:
            self.fail('The module argcomplete is required. Try: sudo pip install argcomplete')
                 
    def test_binary(self):
        """ Checks the binary presence of pygifme """
        assert system('which pygifme 2>&1 > /dev/null') == 0
        
    def test_imagemagick(self):
        """ Checks the binary presence of imagemagick """
        assert system('which convert 2>&1 > /dev/null') == 0
        
    def test_cloudapp(self):
        """ Checks the binary presence of cloudapp """
        # Detect presence of cloudapp (no required at all)
        # gem install cloudapp
        if system('which cloudapp 2>&1 > /dev/null') == 0:
            self.assertTrue(True, 'cloudapp binary detected')
        else:
            self.skipTest('cloudapp no detected. Skipping because not mandatory')

class TestArguments(unittest.TestCase):
    """ Test Arguments """
    
    REMOTE_GIF = 'https://a248.e.akamai.net/camo.github.com/0b546aee911bb34aeaa3109081ec70d15b159d2c/687474703a2f2f662e636c2e6c792f6974656d732f3054306632773243327a335433343377307533372f7075672e676966'
    
    def setUp(self):
        disable_cloud_app()
    
    def tearDown(self):
        enable_cloud_app()
             
    def test_no_files(self):
        """ Test invocation without FILES argument """
        
        try:
            check_output(['pygifme'], stderr = STDOUT)
            self.fail('error: pygifme must run with FILES argument')
        except CalledProcessError as e:
            self.assertNotEqual(e.returncode, EX_OK)
            result = 'the following arguments are required: FILES'
            self.assertIn(result, str(e.output))
    
    def test_unexistant_file(self):
        """ Test invocation with unexistant FILES argument """
        try:
            output = check_output(['pygifme', 'some_unexistant_file'], stderr = STDOUT)
            self.fail('Failed because the file should be unexistant:' + str(output))
        except CalledProcessError as e:
            self.assertNotEqual(e.returncode, EX_OK)
            
            result = 'does not exist'
            self.assertIn(result, str(e.output))
            
        
    def test_one_file(self):
        """ Test invocation with one FILES argument """
        output = check_output(['pygifme', 'test/1.jpg'], stderr = STDOUT)
        
        result = 'You now have a handsome animation at'
        self.assertIn(result, str(output))
    
    def test_two_files(self):
        """ Test invocation with two FILES argument """
        output = check_output(['pygifme', 'test/1.jpg', 'test/2.jpg'], stderr = STDOUT)
                              
        result = 'You now have a handsome animation at'
        self.assertIn(result, str(output))

    def test_global_files(self):
        """ Test invocation with global FILES argument """
        try:
            output = check_output(['pygifme', 'test/*.jpg'], stderr = STDOUT)
            
            result = 'You now have a handsome animation at'
            self.assertIn(result, str(output))
        except CalledProcessError as e:
            self.assertNotEqual(e.returncode, EX_OK)
            self.fail('Failed because:' + str(e.output))
    
    def test_remote_file(self):
        """ Test invocation with remote FILES argument """
        try:
            output = check_output(['pygifme', self.REMOTE_GIF], stderr = STDOUT)
                                  
            result = 'You now have a handsome animation at'
            self.assertIn(result, str(output))
        except CalledProcessError as e:
            self.assertNotEqual(e.returncode, EX_OK)
            self.fail('Failed because:' + str(e.output))
    
    def test_missing_delay(self):
        """ Test invocation with missing DELAY argument """
        try:
            output = check_output(['pygifme', '-d'], stderr = STDOUT)
            self.fail('Failed because the file should be unexistant:' + str(output))
        except CalledProcessError as e:
            self.assertNotEqual(e.returncode, EX_OK)
            
            result = 'expected one argument'
            self.assertIn(result, str(e.output))
        
        try:
            output = check_output(['pygifme', '-d', 'test/1.jpg'], stderr = STDOUT)
            self.fail('Failed because the file should be unexistant:' + str(output))
        except CalledProcessError as e:
            self.assertNotEqual(e.returncode, EX_OK)
            
            result = 'invalid int value'
            self.assertIn(result, str(e.output))
    
    def test_delay(self):
        """ Test invocation with DELAY argument """
        try:
            output = check_output(['pygifme', '-d', '25', 'test/1.jpg'], stderr = STDOUT)
            
            result = 'You now have a handsome animation at'
            self.assertIn(result, str(output))
        except CalledProcessError as e:
            self.assertNotEqual(e.returncode, EX_OK)
            self.fail('Failed because:' + str(e.output))
    
    def test_missing_width(self):
        """ Test invocation with missing WIDTH argument """
        try:
            output = check_output(['pygifme', '-w'], stderr = STDOUT)
            self.fail('Failed because the file should be unexistant:' + str(output))
        except CalledProcessError as e:
            self.assertNotEqual(e.returncode, EX_OK)
            
            result = 'expected one argument'
            self.assertIn(result, str(e.output))
        
        try:
            output = check_output(['pygifme', '-w', 'test/1.jpg'], stderr = STDOUT)
            self.fail('Failed because the file should be unexistant:' + str(output))
        except CalledProcessError as e:
            self.assertNotEqual(e.returncode, EX_OK)
            
            result = 'invalid int value'
            self.assertIn(result, str(e.output))
    
    def test_with(self):
        """ Test invocation with WITH argument """
        try:
            output = check_output(['pygifme', '-w', '200', 'test/1.jpg'], stderr = STDOUT)
            
            result = 'You now have a handsome animation at'
            self.assertIn(result, str(output))
        except CalledProcessError as e:
            self.assertNotEqual(e.returncode, EX_OK)
            self.fail('Failed because:' + str(e.output))
            
    def test_reverse(self):
        """ Test invocation with -r/--reverse argument """
        try:
            output = check_output(['pygifme', '-r', 'test/1.jpg', 'test/2.jpg'], stderr = STDOUT)
            
            result = 'You now have a handsome animation at'
            self.assertIn(result, str(output))
        except CalledProcessError as e:
            self.assertNotEqual(e.returncode, EX_OK)
            self.fail('Failed because:' + str(e.output))
    
    def test_ouput(self):
        """ Test invocation with -o/--output argument """
        try:
            output = check_output(['pygifme', '-o', '/tmp/pygifme', 'test/1.jpg', 'test/2.jpg'], stderr = STDOUT)
            
            result = 'You now have a handsome animation at'
            self.assertIn(result, str(output))
        except CalledProcessError as e:
            self.assertNotEqual(e.returncode, EX_OK)
            self.fail('Failed because:' + str(e.output))
    
    def test_quiet(self):
        """ Test invocation with -q/--quiet argument """
        try:
            output = check_output(['pygifme', '-q', 'test/1.jpg', 'test/2.jpg'], stderr = STDOUT)
            
            result = ''
            self.assertIn(result, str(output))
        except CalledProcessError as e:
            self.assertNotEqual(e.returncode, EX_OK)
            self.fail('Failed because:' + str(e.output))
    
    def test_help(self):
        """ Test invocation with -h/--help argument """
        output = check_output(['pygifme', '-h'], stderr = STDOUT)
        
        result = 'usage: pygifme'
        self.assertIn(result, str(output))
        
        output = check_output(['pygifme', '--help'], stderr = STDOUT)
        
        self.assertIn(result, str(output))
