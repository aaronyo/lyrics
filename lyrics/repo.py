import yaml
import os.path
import re

FIELD_ORDER = ['artist', 'title', 'lyrics-url', 'lyrics']
REPO_DIR = os.path.join( os.path.dirname(__file__), '..', 'data', 'master')

def save(song):
    song_path = _make_song_path(song['artist'], song['title'])
    _dump(song, open(song_path, 'w'))

def load(artist, title, default):
    song_path = _make_song_path(artist, title)
    if os.path.exists(song_path):
        return yaml.load( open(song_path) )
    else:
        return default
    
def _make_song_path(artist, title):
    path = "%(artist)s-%(title)s" % locals()
    path = re.sub('[^\w]+', '-', path).lower()
    path = path + '.yaml'
    return os.path.join(REPO_DIR, path)

def _dump(song, out):
    # Doesn't look easy to get the yaml dumper to dump my
    # songs in a highly readable way, so rolling my own
    # yaml serialization for now.
    s = ''
    for k in FIELD_ORDER:
        if k not in song:
            continue
            
        s += k + ': '
        if k == 'lyrics':
            lyrics = re.sub(r'\n', r'\n  ', song['lyrics'])
            s += '|'+lyrics
        else:
            s += song[k] + "\n"
    out.write(s)