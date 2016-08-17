#!/usr/bin/env python

"""
This is an example of a simple command line client for Spotify using pyspotify.

You can run this file directly::

    python shell.py

Then run the ``help`` command on the ``spotify>`` prompt to view all available
commands.
"""

import requests
from requests.auth import HTTPDigestAuth
import json


class SpotifyAPI():

    base_url = "https://api.spotify.com/v1"
    tracklist = []

    def __init__(self):
        pass

    def getAlbum(self, spotify_uri):
        url = self.base_url + "/albums/" + spotify_uri
        response = requests.get(url, verify=True)
        print (response)

        if (response.ok):

            jData = json.loads(response.content)
            for track in jData["tracks"]["items"]:
                self.tracklist.append(track["uri"])
            return self.tracklist

        else:
            response.raise_for_status()

    #def getPlaylist(self, spotify_user, spotify_uri):
    #        url = self.base_url + "/user/" + spotify_user + "/playlist/" + spotify_uri
    #        response = requests.get(url, verify=True)
    #        print (response)
    #
    #        if (response.ok):
    #
    #           jData = json.loads(response.content)
    #            for track in jData["tracks"]["items"]:
    #                self.tracklist.append(track["uri"])
    #            return self.tracklist
    #
    #        else:
    #            response.raise_for_status()

    #def getDetails(self):

