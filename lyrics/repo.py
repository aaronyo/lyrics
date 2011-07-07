import yaml
import os.path
import re
import copy

FIELD_ORDER = ['artist', 'title', 'peak-year', 'tags', 'lyrics-url', 'lyrics']
REPO_DIR = os.path.join( os.path.dirname(__file__), '..', 'data', 'songs')

def save(song):
    song_path = _make_song_path(song['artist'], song['title'])
    _dump(song, open(song_path, 'w'))

def load(artist, title, default=None):
    song_path = _make_song_path(artist, title)
    if os.path.exists(song_path):
        y = yaml.load( open(song_path) )
        return y
    else:
        return default

def _listdir_fullpath(d):
    # credit: http://stackoverflow.com/questions/120656/directory-listing-in-python
    #         user: giltay
    return [os.path.join(d, f) for f in os.listdir(d)]        

def list():
    song_list = []
    for f in _listdir_fullpath( REPO_DIR ):
        y = yaml.load( open(f) )
        song_list.append( (y.get('peak-year', None), y['artist'], y['title']) )
        song_list.sort()
    return song_list
    
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
    s = u''
    for k in FIELD_ORDER:
        if k not in song:
            continue
            
        s += k + ': '
        value = song.pop(k)
        if k == 'lyrics':
            lyrics = re.sub(r'\r', r'', value)
            lyrics = re.sub(r'\n\ *', r'\n  ', lyrics)
            s += u'|'+lyrics
        elif k == 'tags':
            s += '\n'
            for tag in value:
                s += '    - %s\n' % str(tag)
        else:
            s += unicode(value) + "\n"
    if song:
        raise ValueError("Song contains unrecognized fields: %s" % s)
    out.write(s.encode('utf-8'))