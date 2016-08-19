
"""

 nfcReader.py for SpotifyBox project

 Made by Antoine Guittet
 Email <ag612@kent.ac.uk>

 University Of Kent

 This class is designed as an external components, able at any time to be change for an other NFC Reader.
 In this project, the PN532 NFC reader from Adafruit has been used and this class is based on the opensource driver
 provided with it

"""

# Example of detecting and reading a block from a MiFare NFC card.
# Author: Tony DiCola
# Copyright (c) 2015 Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import string
import Adafruit_PN532 as PN532

class Reader():

    def __init__(self):
        printable = set(string.printable)

class NFCReader(Reader):

    _CS = 0
    _MOSI = 0
    _MISO = 0
    _SCLK = 0

    reader = ""
    printable = ""

    def __init__(self):
        self.printable = set(string.printable)

        self._CS = 18
        self._MOSI = 23
        self._MISO = 24
        self._SCLK = 25

        self.reader = PN532.PN532(cs=self._CS, sclk=self._SCLK, mosi=self._MOSI, miso=self._MISO)

    def begin(self):
        # Call begin to initialize communication with the PN532.
        self.reader.begin()
        ic, ver, rev, support = self.reader.get_firmware_version()
        print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

        self.reader.SAM_configuration()

