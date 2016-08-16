#!/usr/bin/env python

"""
This is an example of a simple command line client for Spotify using pyspotify.

You can run this file directly::

    python shell.py

Then run the ``help`` command on the ``spotify>`` prompt to view all available
commands.
"""

from __future__ import unicode_literals

import logging

import spotify
import spotifySDK
import spotifyAPI
import nfcReader

import binascii
import sys
import string
import ledDriver


class SpotifyBox():

    _sdk = ""
    _nfcReader = ""
    _led = ""
    _config = ""
    _api = ""

    queue = []
    
    col = [0x00FFFF]
    def __init__(self):
        print("Log | _init_SpotifyBox_ | Start")
        self._config = spotify.Config()
        self._config.load_application_key_file('spotify_appkey.key')
        self._nfcReader = nfcReader.NFCReader()
        self._nfcReader.begin()
        self._led = ledDriver.LedDriver()
        self._led.setReady()
        self._api = spotifyAPI.SpotifyAPI()
        self._sdk = spotifySDK.SpotifySDK()
        print("Log | _init_SpotifyBox_ | End Success")

    def passive_reading(self, uid):
        # Check if a card is available to read.

        print('Found card with UID: 0x{0}'.format(binascii.hexlify(uid)))
        # Authenticate block 4 for reading with default key (0xFFFFFFFFFFFF).
        # if not pn532.mifare_classic_authenticate_block(uid, 4, PN532.MIFARE_CMD_AUTH_B,
        #                                               [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]):
        #    print('Failed to authenticate block 4!')
        #    continue
        # Read block 4 data.
        i = 7
        payload = ""
        try:
            #while self._nfcReader.reader.mifare_classic_read_block(i) is not None:
            while i <= 15:
                data = self._nfcReader.reader.mifare_classic_read_block(i)
                buffer = format(binascii.hexlify(data[:4]))
                buffer = binascii.unhexlify(buffer)
                print(buffer)
                payload = payload + buffer
                # print((binascii.hexlify(data[:8]).decode('hex')))
                i = i + 1
            return (payload)
        except:
            print ("reading error")
            return ('error')
            # Note that 16 bytes are returned, so only show the first 4 bytes for the block.
            # print('Read block 4: 0x{0}'.format(binascii.hexlify(data[:4])))
            # Example of writing data to block 4.  This is commented by default to
            # prevent accidentally writing a card.
            # Set first 4 bytes of block to 0xFEEDBEEF.
            # data[0:4] = [0xFE, 0xED, 0xBE, 0xEF]
            # # Write entire 16 byte b   lock.
            # pn532.mifare_classic_write_block(4, data)
            # print('Wrote to block 4, exiting program!')
            # # Exit the program to prevent continually writing to card.
            # sys.exit(0)

    def checkUri(self, uri):
        print uri
        track = ''
        uriParsed = uri.split(':')
        if uriParsed[0] == 'spotify':
            if uriParsed[1] == 'album':
                self.queue = self._api.getAlbum(uriParsed[2])
                self._sdk.queue = self.queue
                track = self._sdk.queue.pop()
            elif uriParsed[1] == 'playlist':
                print ('playlist')
            elif uriParsed[1] == 'track':
                track = uri
        return track
        
    def run(self):
        current_spotify_uri = None
        printable = set(string.printable)
        logging.basicConfig(level=logging.INFO)

        # Main loop to detect cards and read a block.
        print('Log | _mainLoop_ | Start')
        while True:
            uid = self._nfcReader.reader.read_passive_target()
            # Try again if no card is available.new
            if uid is None:
                print ('toto')
                continue

            new_spotify_uri = self.passive_reading(uid)
            current_spotify_uri = self.checkUri(new_spotify_uri)
            if new_spotify_uri is not None and new_spotify_uri is not current_spotify_uri:
                payload = filter(lambda x: x in printable, current_spotify_uri)
                self._led.setReading()
                self._led.setReady()
                self._sdk.do_play_uri(current_spotify_uri)
              
