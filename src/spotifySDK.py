#!/usr/bin/env python

"""

 spotifySDK.py for SpotifyBox project

 Made by Antoine Guittet
 Email <ag612@kent.ac.uk>

 University Of Kent


 Call from the Spotify box software to the original Spotify SDK LibSpotify,
 through a python Lib pyspotfy - https://pyspotify.modipy.com

"""

from __future__ import unicode_literals

import cmd
import logging
import threading

import spotify


class SpotifySDK(cmd.Cmd):

    logger = logging.getLogger('Phygipy')
    queue  = []

    def __init__(self):
        cmd.Cmd.__init__(self)

        self.logged_in = threading.Event()
        self.logged_out = threading.Event()
        self.logged_out.set()

        self.session = spotify.Session()
        self.session.on(
            spotify.SessionEvent.CONNECTION_STATE_UPDATED,
            self.on_connection_state_changed)
        self.session.on(
            spotify.SessionEvent.END_OF_TRACK, self.on_end_of_track)

        # Set Alsamixer as audio output
        try:
            self.audio_driver = spotify.AlsaSink(self.session)
        except ImportError:
            self.logger.warning(
                'No audio sink found; audio playback unavailable.')

        self.event_loop = spotify.EventLoop(self.session)
        self.event_loop.start()

        #replace username and password with your own credentials
        self.session.login('username', 'password', remember_me=True)
        self.logged_in.wait()

    def listen(self):
        self.cmdloop()

    def on_connection_state_changed(self, session):
        if session.connection.state is spotify.ConnectionState.LOGGED_IN:
            self.logged_in.set()
            self.logged_out.clear()
        elif session.connection.state is spotify.ConnectionState.LOGGED_OUT:
            self.logged_in.clear()
            self.logged_out.set()

    def on_end_of_track(self, session):
        if self.queue:
            track = self.queue.pop()
            self.do_play_uri(track)
        else:
            self.session.player.play(False)

    def do_login(self, line):
        "login <username> <password>"
        tokens = line.split(' ', 1)
        if len(tokens) != 2:
            self.logger.warning("Wrong number of arguments")
            return
        username, password = tokens
        self.session.login(username, password, remember_me=True)
        self.logged_in.wait()

    def play_uri(self, line):

        # Last verification if the uri is correct
        if 'track' in line :
            if not self.logged_in.is_set():
                self.logger.warning('You must be logged in to play')
                return

            try:
                track = self.session.get_track(line)
                track.load()
            except (ValueError, spotify.Error) as e:
                self.logger.warning(e)
                return
            self.logger.info('Loading track into player')
            self.session.player.load(track)
            self.logger.info('Playing track')
            self.session.player.play()
        else:
            if 'album' in line :
                self.logger.warning('Not able to play album')
                return
            if 'playlist' in line :
                self.logger.warning('Not able to play playlist')
                return