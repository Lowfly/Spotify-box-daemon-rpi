#!/usr/bin/env python

"""

 spotifyAPI class test file

"""

import sys
sys.path.insert(0, '../src/')
import spotifyAPI
import time


print("Starting tests")

api = spotifyAPI.SpotifyAPI()

print("Test get valid album uri - Should return list of tracks")

print(api.getAlbum('spotify:album:1jfBSA8KgMLol7lahnq8wv'))
time.sleep(3)


print("Test not valid album uri - Should print error")
print(api.getAlbum('spotify:album:1jfBSAf8KgMLolfwiw8wv'))

time.sleep(3)

print("Test done")
