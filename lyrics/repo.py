import yaml
import os.path
import re
import copy

FIELD_ORDER = ['artist', 'title', 'peak-year', 'tags', 'lyrics-url', 'lyrics']
REPO_DIR = os.path.join( os.path.dirname(__file__), '..', 'data', 'songs')

def save(song):
    song_path = _make_song_path(song['artist'], song['title'])
    _dump(song, open(song_path, 'w'))

def load(artist, title, default):
    song_path = _make_song_path(artist, title)
    if os.path.exists(song_path):
        print "Loading %s" % title
        y = yaml.load( open(song_path) )
        print y.keys()
        return y
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
    song = copy.deepcopy(song)
    print song.keys()
    s = ''
    for k in FIELD_ORDER:
        if k not in song:
            continue
            
        s += k + ': '
        value = song.pop(k)
        if k == 'lyrics':
            lyrics = re.sub(r'\r', r'', value)
            lyrics = re.sub(r'\n\ *', r'\n  ', lyrics)
            s += '|'+lyrics
        elif k == 'tags':
            s += '\n'
            for tag in value:
                s += '    - %s\n' % str(tag)
        else:
            s += str(value) + "\n"
    if song:
        raise ValueError("Song contains unrecognized fields: %s" % s)
    out.write(s)