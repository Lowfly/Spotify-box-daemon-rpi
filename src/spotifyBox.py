#!/usr/bin/env python

"""
This is an example of a simple command line client for Spotify using pyspotify.

You can run this file directly::

    python shell.py

Then run the ``help`` command on the ``spotify>`` prompt to view all available
commands.
"""

from __future__ import unicode_literals

import cmd
import logging
import threading

import spotifySDK
from subprocess import call



class SpotifyBox():

    _sdk = spotifySDK();

    def __init__(self):

    def listen(self):
        print("toto");