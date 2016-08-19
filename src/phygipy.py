#!/usr/bin/env python

"""

 phygipy.py for SpotifyBox project

 Made by Antoine Guittet
 Email <ag612@kent.ac.uk>

 University Of Kent


 Entry point of the SpotifyBox. Call and run the main routine

"""


from __future__ import unicode_literals

from subprocess import call
import logging
import spotifyBox

    
if __name__ == '__main__':

    #Set the log file, usefull when the box is run without monitor screen
    logging.basicConfig(filename='phygipy_log.log', level=logging.DEBUG, format='%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s')
    logger = logging.getLogger('Phygipy')
    logging.info('Start Phygipy')

    call(["sudo", "amixer", "cset", "numid=3", "1"])
    logging.info('Load Spotify Box')

    #Call the main routine
    spotifybox = spotifyBox.SpotifyBox()
    spotifybox.run()
