import pytest
from spotify_api.spotify_api_helpers import similar, get_album_art_url, add_album_art_to_albums
no_img_found = 'https://img.discogs.com/knYf8Jh6i4fearhTLJX1wN9PKs8=/fit-in/300x300/filters:strip_icc():format(jpeg):mode_rgb():quality(40)/discogs-images/R-1334150-1515948978-5427.jpeg.jpg'
# tests that a no image_found url is returned
# based on assumption that there is no album called "_____" by Rick Astley
def test_get_album_art_album_not_found():
    result_url = get_album_art_url("_____", 'Rick Astley')
    assert result_url == no_img_found


# test that identical strings produce ratio of 0
def test_similar_identical_strings():
    assert(similar('ababab', 'ababab') == float(0))

def test_similar_different_strings():
    assert(similar('abc', 'xyz') == float(0))
