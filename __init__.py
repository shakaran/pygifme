# -*- coding: utf-8; tab-width: 4; mode: python -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: t -*
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

__package__ = 'pygifme'
__version__ = '0.1'
__all__ = ['.pygifme']

def main(): # For setuptools entry point
    from . import pygifme
    pygifme.main()