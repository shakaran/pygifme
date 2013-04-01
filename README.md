# pygifme

![pug](http://f.cl.ly/items/0T0f2w2C2z3T343w0u37/pug.gif)

[![Travis status build](https://secure.travis-ci.org/shakaran/pygifme.png?branch=master)](http://travis-ci.org/shakaran/pygifme)

## Fucking animations. You need them.

pygifme is a simple command line tool to generate animated GIFs. It is a python port from the original ruby script gifme created by [@holman](https://twitter.com/holman)

## Installation

Install pygifme:

    pip3 install pygifme

You also can install via setup.py file:

    python3 setup.py install

You'll also need to install ImageMagick. 

On GNU/LINUX Debian systems:

    sudo apt-get install imagemagick

On OS X, this is easy using Homebrew:

    brew install imagemagick

This script is for Python >= 3.0. It also needs python module argcomplete if
you wish pygifme autocompletion in command line.

You can install with:

    sudo pip3 install argcomplete

Or via requirements.txt file:

   sudo pip3 install -r requirements.txt --use-mirrors

## Usage

    pygifme ~/Desktop/1.png ~/Desktop/2.png
    You now have a handsome animation at ~/Desktop/animated.gif

You can also glob, of course:

    pygifme ~/Desktop/*.jpg
    You now have a handsome animation at ~/Desktop/animated.gif

## CloudApp

Once your animation is finished up, we'll try to upload it to
[CloudApp](http://www.getcloudapp.com). If you have 
[`cloudapp`](https://github.com/holman/dotfiles/blob/master/bin/cloudapp)
script installed, we'll use that, otherwise we'll just skip this whole step.

## Super Advanced Usage

On some gifs, it's nice to have a smooth loop, so when it ends there's not a
jarring leap from the last frame to the first frame again. Use the `--reverse`
switch to create the animation like normal, and then reverse the frames and add
them to the animation so it looks like one smooth motion and back again.

    pygifme FILES --reverse

If you pass in a URL of a gif instead of FILES, we'll download that gif, split
it into its constituent frames, and let you recreate it. For example, you could
take a gif you find online and give it that `--reverse` look:

    pygifme http://tumblr.com/some-crazy.gif --reverse

You can also resize shit. We default to 500 pixels, but do whatever the fuck
you want.

    pygifme http://tumblr.com/some-crazy.gif --width=1000

For other options, check out the help:

    pygifme -h

## History

If you're curious, gifme was initially a few-line shell script in [Zach Holman
dotfiles](https://github.com/holman/dotfiles). Eventually it became clear that
animation is a fundamental part of our society, and I split it out into its own
tiny project.

If you're curious, Zach Holman featured the older gifme version [in a
screencast](http://zachholman.com/2011/01/automating-inefficiencies/) Zach Holman made
that describes how animated gifs are an integral part of working at GitHub.

I made this python port just for fun and practice ruby to python porting.

## Running unit tests

This is a simple script, but it can have unexpect behaviour doing weird things
with ImageMagick backend. So, if you want ensure the common behaviour, then you
can run the unit testing battery with:

    python3 -m unittest test

Also from setup.py (recommended):

    sudo python3 setup.py test

## Much Love

From [@holman](https://twitter.com/holman). Zach Holman loves you.

## About

Mantainer [@shakaran87](https://twitter.com/shakaran87).
