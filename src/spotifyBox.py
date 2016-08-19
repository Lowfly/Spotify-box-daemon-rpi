#!/usr/bin/env python

"""

 spotifyBox.py for SpotifyBox project

 Made by Antoine Guittet
 Email <ag612@kent.ac.uk>

 University Of Kent

 Main class of the SpotifyBox project. Represent the box itself, and contains
 all its sensors. We can easily add a new sensor or new functionality.

"""


from __future__ import unicode_literals

import logging
import binascii
import string
import logging

import spotify
import spotifySDK
import spotifyAPI

import nfcReader
import ledDriver


class SpotifyBox():

    _sdk = ""
    _nfcReader = ""
    _led = ""
    _config = ""
    _api = ""

    queue = []

    def __init__(self):

        # Initialize logger
        logger = logging.getLogger('Phygipy')
        logging.info('Init SpotifyBox')

        # Load the spotify SDK key
        self._config = spotify.Config()
        self._config.load_application_key_file('spotify_appkey.key')

        # Initialize NFC Reader
        self._nfcReader = nfcReader.NFCReader()
        self._nfcReader.begin()

        # Initialize led and blink green
        self._led = ledDriver.LedDriver()
        self._led.setReady()

        #Initialize API and SDK
        self._api = spotifyAPI.SpotifyAPI()
        self._sdk = spotifySDK.SpotifySDK()

    def passive_reading(self, uid):
        # Check if a card is available to read.
        print('Card UID: 0x{0}'.format(binascii.hexlify(uid)))
    
        i = 7
        payload = ""

        # Try to extract the payload from the NFC tag
        try:
            while i <= 15:
                data = self._nfcReader.reader.mifare_classic_read_block(i)
                buffer = format(binascii.hexlify(data[:4]))
                buffer = binascii.unhexlify(buffer)
                print(buffer)
                payload = payload + buffer
                i = i + 1
            return payload

        #In case of error - return None
        except:
            return None

    def checkUri(self, uri):

        # Check the validity of a given uri. To be valid, a given uri
        # must contains spotify + track or album + _id
        #
        # Playlist are not supported due to the need to be OAuth Authenticated to request them.

        track = ''
        uriParsed = uri.split(':')
        if uriParsed[0] == 'spotify':

            # If it is an album, we request the SpotifyAPI to get all the tracks of this album,
            # then we replace the current playing queue by those
            if uriParsed[1] == 'album':
                self.queue = self._api.getAlbum(uriParsed[2])
                self._sdk.queue = self.queue
                track = self._sdk.queue.pop()

            # If it is a track, we clean the playing queue.
            elif uriParsed[1] == 'track':
                self._sdk.queue = []
                track = uri
            else:
                return None
            
        # The track to play is returned, in case of not valid type or uri, we return None
        return track
        
    def run(self):
        
        spotify_uri = None
        payload = None
        printable = set(string.printable)
        logging.basicConfig(level=logging.INFO)

        # The main routine start here. It will passively check if a tag is readable. If not the routine continue
        # If a valid uri has been read, the led will blink with the color blue and the music will start to be played
        # in a new thread. In case of error, a red led will blink and the routine continue.
        
        print('Log | _mainLoop_ | Start')
        while True:

            # Set the NFC reader to be in passive reading
            uid = self._nfcReader.reader.read_passive_target()
            
            # Routine continue if no card is available
            if uid is None:
                continue
            
            else:
                # Extract the payload
                payload = self.passive_reading(uid)
                if payload is None:
                    self._led.setError()
                    continue
                
                else:
                    # Check the validity of the payloard
                    spotify_uri = self.checkUri(payload)

                    if spotify_uri is None:
                        self._led.setError()
                        continue

                    # Set led blinking and color
                    self._led.setReading()
                    self._led.setReady()

                    # Play the given uri
                    self._sdk.play_uri(spotify_uri)
              
