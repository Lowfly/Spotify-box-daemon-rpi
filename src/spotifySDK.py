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

import spotify
from subprocess import call



class SpotifySDK(cmd.Cmd):

    doc_header = 'Commands'
    prompt = 'spotify> '

    logger = logging.getLogger('shell.commander')

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

        try:
            self.audio_driver = spotify.AlsaSink(self.session)
        except ImportError:
            self.logger.warning(
                'No audio sink found; audio playback unavailable.')

        self.event_loop = spotify.EventLoop(self.session)
        self.event_loop.start()

        self.session.login('11140070406', '2p,pvesb', remember_me=True) # Todo: Change to put in creditentials file
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
        print ("END OF TRACK")
        self.session.player.play(False)

    def precmd(self, line):
        if line:
            self.logger.debug('New command: %s', line)
        return line

    def emptyline(self):
        pass

    def do_debug(self, line):
        "Show more logging output"
        print('Logging at DEBUG level')
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

    def do_info(self, line):
        "Show normal logging output"
        print('Logging at INFO level')
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

    def do_warning(self, line):
        "Show less logging output"
        print('Logging at WARNING level')
        logger = logging.getLogger()
        logger.setLevel(logging.WARNING)

    def do_EOF(self, line):
        "Exit"
        if self.logged_in.is_set():
            print('Logging out...')
            self.session.logout()
            self.logged_out.wait()
        self.event_loop.stop()
        print('')
        return True

    def do_login(self, line):
        "login <username> <password>"
        tokens = line.split(' ', 1)
        if len(tokens) != 2:
            self.logger.warning("Wrong number of arguments")
            return
        username, password = tokens
        self.session.login(username, password, remember_me=True)
        self.logged_in.wait()

    def do_relogin(self, line):
        "relogin -- login as the previous logged in user"
        try:
            self.session.relogin()
            self.logged_in.wait()
        except spotify.Error as e:
            self.logger.error(e)

    def do_logout(self, line):
        "logout"
        self.session.logout()
        self.logged_out.wait()

    def do_play_uri(self, line):
        "play <spotify track uri>"
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

    def do_pause(self, line):
        self.logger.info('Pausing track')
        self.session.player.play(False)

    def do_resume(self, line):
        self.logger.info('Resuming track')
        self.session.player.play()

    def do_stop(self, line):
        self.logger.info('Stopping track')
        self.session.player.play(False)
        self.session.player.unload()


    def do_seek(self, seconds):
        "seek <seconds>"
        if not self.logged_in.is_set():
            self.logger.warning('You must be logged in to seek')
            return
        if self.session.player.state is spotify.PlayerState.UNLOADED:
            self.logger.warning('A track must be loaded before seeking')
            return
        self.session.player.seek(int(seconds) * 1000)
