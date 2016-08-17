#!/usr/bin/env python

"""

Entrance of the SpotifyBox program, init and run the SpotifyBox class

"""


from __future__ import unicode_literals


from subprocess import call
import spotifyBox

if __name__ == '__main__':
    call(["sudo", "amixer", "cset", "numid=3", "1"])
    spotifybox = spotifyBox.SpotifyBox()
    spotifybox.run()
