from difflib import SequenceMatcher
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)

'''
helper function to compare similarity of strings as a ratio
'''
def similar(a, b):
    return float(SequenceMatcher(None, a, b).ratio())

'''
get link to album art provided by spotify
wraps a spotify search query on an album and artist and compares retrieved results to ensure album art is for correct album
'''
def get_album_art_url(target_album_name, target_artist_name):
    query = target_album_name.replace(' ', '+')
    no_img_found = 'https://img.discogs.com/knYf8Jh6i4fearhTLJX1wN9PKs8=/fit-in/300x300/filters:strip_icc():format(jpeg):mode_rgb():quality(40)/discogs-images/R-1334150-1515948978-5427.jpeg.jpg'
    
    try:
        results = sp.search(query, 1, 0, 'album', None)
        artist_name = results['albums']['items'][0]['artists'][0]['name']
        album_name = results['albums']['items'][0]['name']
        album_art_url = results['albums']['items'][0]['images'][0]['url']
        
    except:
        return no_img_found
    
    # 0.8 should be low enough similarity ratio to ensure names like "travis scott" and "Travi$ Scott" are matched
    if similar(artist_name.lower(), target_artist_name.lower()) > 0.8 and similar(album_name.lower(), target_album_name.lower()) > 0.8:
        return  album_art_url
    else:
        return no_img_found

'''
helper function to add the album art url to a list of albums
'''
def add_album_art_to_albums(albums):
    for album in albums:
        album['album_art'] = get_album_art_url(album['title'], album['artist'])

