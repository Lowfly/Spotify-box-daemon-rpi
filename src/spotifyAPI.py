#!/usr/bin/env python

"""

 spotifyApi.py for SpotifyBox project

 Made by Antoine Guittet
 Email <ag612@kent.ac.uk>

 University Of Kent


 Service for API calls, could be extend with OAuth authentication for Playlist requests

"""

import requests
from requests.auth import HTTPDigestAuth
import json


class SpotifyAPI():

    base_url = "https://api.spotify.com/v1"
    tracklist = []

    def __init__(self):
        pass

    # Get list of tracks in the given album
    def getAlbum(self, spotify_uri):
        url = self.base_url + "/albums/" + spotify_uri
        response = requests.get(url, verify=True)

        if (response.ok):
            jData = json.loads(response.content)
            for track in jData["tracks"]["items"]:
                self.tracklist.insert(0, track["uri"])
            return self.tracklist

        else:
            response.raise_for_status()



