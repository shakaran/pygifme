#!/usr/bin/env python3
# -*- coding: utf-8; tab-width: 4; mode: python -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: t -*
# vi: set ft=python sts=4 ts=4 sw=4 noet

# pylint: disable-msg=R0903,C0103,C0301

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

# PYTHON_ARGCOMPLETE_OK

def main():
    from os import system, mkdir, listdir, environ, path, chdir, getcwd, \
                   EX_USAGE, EX_DATAERR, EX_CONFIG, EX_CANTCREAT
    from time import gmtime, strftime
    from sys import exit, path as spath
    from argparse import ArgumentParser, ONE_OR_MORE, HelpFormatter
    from argcomplete import autocomplete
    
    # Avoid problems with /usr/local/bin first in sys.path
    if path.dirname(__file__) == spath[0]:
        spath.append(spath[0])
        del spath[0]
    
    try:
        from pygifme import __version__
    except ImportError as e:
        #from . import __version__
        __version__ = '0.1' # @Fixme: Bad package import from /usr/local/bin/pygifme.py
        
    description = '  FILES can be listed out, like `file1.jpg file2.jpg`, or it\n' \
                  '  can be a normal shell glob, like `*.jpg`.'
            
    parser = ArgumentParser(
                             prog                  = 'pygifme',
                             description           = description,
                             epilog                = None,
                             parents               = [],
                             formatter_class       = HelpFormatter,
                             prefix_chars          = '-',
                             fromfile_prefix_chars = None,
                             argument_default      = None,
                             conflict_handler      = 'error',
                             add_help              = True,
                            )
    
    def valid_directory(directory):
        if path.exists(directory):
            if path.isdir(directory):
                return directory
            else:
                parser.error('Path {0} is not a directory'.format(directory))
                return directory
        else:
            parser.error('Directory path {0} does not exist'.format(directory))
                       
    parser.add_argument('-r', '--reverse',
                        action         = 'store_true',
                        dest           = 'reverse',
                        default        = False,
                        help           = 'Reverse the GIF to make it loopable')
    
    parser.add_argument('-o', '--output',
                        action         = 'store',
                        metavar        = '/path/to/output',
                        type           = lambda d:valid_directory(d),
                        dest           = 'output',
                        choices       = None,
                        help           = 'Set the animation\'s output directory')
    
    parser.add_argument('-d', '--delay',
                        action         = 'store',
                        metavar        = 'DELAY',
                        dest           = 'delay',
                        default        = 20,
                        type           = int,
                        choices        = None,
                        help           = 'Set the delay between frames (default: 20)')
    
    parser.add_argument('-w', '--width',
                        action         = 'store',
                        metavar        = 'PIXELS',
                        dest           = 'width',
                        default        = 500,
                        type           = int,
                        choices        = None,
                        help           = 'Set the width of the image (default: 500px)')
    
    parser.add_argument('-q', '--quiet',
                        action         = 'store_true',
                        dest           = 'quiet', 
                        default        = False,
                        help           = 'Don\'t print status messages to stdout')
    
    parser.add_argument(option_strings = ['FILES'], 
                        metavar        = 'FILES', 
                        nargs          = ONE_OR_MORE,
                        type=str,
                        dest           = 'FILES',
                        help           = 'One or more files to process')
    
    parser.add_argument('-v', '--version', 
                        action  ='version',
                        version ='%(prog)s {version}'.format(version = __version__),
                        help    = 'Shows the program version')
    
    autocomplete(parser)
    args = parser.parse_args()
    
    #print(vars(args)) # For debugging
    
    if system("which convert 2>&1 > /dev/null") != 0:
        parser.error('You need to install ImageMagick first.\n\n' \
               'If you\'re on GNU/LINUX Debian systems, this should be as easy as:\n'\
               '  sudo apt-get install imagemagick\n' \
               'If you\'re on a Mac, this should be as easy as:\n' \
               '  brew install imagemagick')
        exit(EX_CONFIG)
        
    if not args.FILES: # no files given
        parser.error('no FILES given to process')
        exit(EX_USAGE)
    else:
        for pfile in args.FILES:
            if pfile[0:4] != 'http': # skip remote files
                if path.exists(pfile):
                    if not path.isfile(pfile):
                        parser.error('{0} is not a valid file'.format(pfile))
                else:
                    import glob
                    result_glob = glob.glob(pfile)
                    if not result_glob:
                        parser.error('File {0} does not exist'.format(pfile))
                    else:
                        for gfile in result_glob:
                            if path.exists(gfile):
                                if not path.isfile(gfile):
                                    parser.error('{0} is not a valid file'.format(gfile))
                            else:
                                parser.error('File {0} does not exist'.format(gfile))
        
    # WORKING WITH REMOTE FILES
    if args.FILES[0][0:4] == 'http':
        from urllib import request
        from shutil import rmtree
        
        if path.exists('/tmp/pygifme'):
            rmtree('/tmp/pygifme')
            
        mkdir('/tmp/pygifme', 0o777)
        
        local_path = '/tmp/downloaded-pygifme.gif'
    
        with open(local_path, mode='wb') as wfile:
            remote_file = request.urlopen(args.FILES[0]).read()
            wfile.write(remote_file)
    
        wd = getcwd()
        chdir('/tmp/pygifme')
        status = system('convert {0} -coalesce frame_%03d.gif'.format(local_path))
        chdir(wd)
        
        if status != 0:
            parser.error('Could not process remote file {0}'.format(local_path))
            exit(EX_DATAERR)
        
        del args.FILES[0]
        args.FILES += [path.join('/tmp/pygifme/', f) for f in listdir('/tmp/pygifme/')]
    
    if args.reverse:
        args.FILES += args.FILES[1:-2]
    
    if not args.output:
        import subprocess
        desktop = str(subprocess.check_output(['xdg-user-dir', 'DESKTOP'], universal_newlines = True)).strip()
        
        if not desktop:
            home = environ.get('HOME')
            if not home:
                home = '/tmp/pygifme'
                mkdir(home, 0o777)
            else:
                home = '{0}/Desktop'.format(home)
        else:
            home = desktop

        args.output = home
    
    args.output = str(args.output) + '/animated-{0}.gif'.format(strftime('%F_%Hh-%Mm-%Ss', gmtime()))
               
    cmd = 'convert -delay {0} -loop 0 -resize {1} -layers OptimizeTransparency {2} {3}'.format(int(args.delay), int(args.width), ' '.join(args.FILES), str(args.output))
    if system(cmd) == 0:
        if not args.quiet:
            print('You now have a handsome animation at {0}'.format(args.output))
    else:
        parser.error('Something broke when we were animating your gif. Shit.')
        exit(EX_CANTCREAT)
    
    if system('which cloudapp 2>&1 > /dev/null') == 0 and not environ.get('DISABLE_CLOUPAPP'):
        if not args.quiet:
            print('Now we\'re uploading it to CloudApp')
        system('cloudapp {0}'.format(args.output))

if __name__ == '__main__':
    main()