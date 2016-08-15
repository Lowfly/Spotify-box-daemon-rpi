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

import spotifySDK
import spotify
import nfcReader

import binascii
import sys
import string


class SpotifyBox():

    _sdk = ""
    _nfcReader = ""
    _config = ""

    def __init__(self):
        print("Log | _init_SpotifyBox_ | Start")
        self._config = spotify.Config()
        self._config.load_application_key_file('spotify_appkey.key')
        self._nfcReader = nfcReader.NFCReader()
        self._nfcReader.begin()
        print("Log | _init_SpotifyBox_ | End Success")



    def run(self):
        printable = set(string.printable)
        logging.basicConfig(level=logging.INFO)
        _sdk = spotifySDK.SpotifySDK()
        _sdk.do_play_uri('spotify:track:4n4Z8qVlDkEnfX68PYJfJu')
        #_sdk.listen()
        #_sdk.cmdloop()
        # Main loop to detect cards and read a block.
        print('Waiting for MiFare card...')
        while True:
                # Check if a card is available to read.
            uid = self._nfcReader.reader.read_passive_target()
                # Try again if no card is available.
            if uid is None:
                continue
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
                while self._nfcReader.reader.mifare_classic_read_block(i) is not None:
                    data = self._nfcReader.reader.mifare_classic_read_block(i)
                    buffer = format(binascii.hexlify(data[:4]))
                    buffer = binascii.unhexlify(buffer)
                    print(buffer)
                    payload = payload + buffer
                    # print((binascii.hexlify(data[:8]).decode('hex')))
                    i = i + 1
                payload = filter(lambda x: x in printable, payload)
                print (payload)
            except :
                print ("reading error")
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