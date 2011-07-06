import urllib2
import optparse
import yaml
import re
from pprint import pprint
import time
import os.path
import repo

import parse

CACHE_DIR = os.path.join( os.path.dirname(__file__), '..', 'data', 'cache')
LYRICS_HOST = 'http://www.lyricstime.com/'

def main():
    parser = optparse.OptionParser()
    parser.usage = 'usage: %prog SONG_URL|SONG_LIST_FILE ...'
    parser.add_option('-f', '--force', action='store_true', default=False)
    parser.add_option('-r', '--no-request', action='store_true', default=False)

    (options, args) = parser.parse_args()
    

    if not args:
        parser.print_help()
        return
    
    cmd = args.pop(0)
    if cmd == 'update':
        update_cmd(args, options)

def update_cmd(args, options):
    if args[0].endswith('yaml'):
        song_list_file = args[0]
        song_list = load_song_list( open(song_list_file) )
        for s in song_list:
            page = get_page(s['artist'], s['title'], url=s.get('lyrics-url', None), request=not options.no_request)
            if page == None:
                continue
            lyrics = parse.extract_lyrics(page)
            song = repo.load(s['artist'], s['title'], default=s)
            song['lyrics'] = lyrics
            repo.save(song)

    elif args[0].startswith('http://'):
        song_url = args[0]
        lyrics_page = get_lyrics_page(song_url)
        print parse.parse_lyrics(song_url)

    else:
        parser.print_help()
        return
        

def get_page(artist, title, url=None, request=True):
    cache_filename = make_song_path(artist, title)
    cache_path = os.path.join(CACHE_DIR, cache_filename)
    if not request and not os.path.exists(cache_path):
        return None

    if not os.path.exists(cache_path):
        song_url = url or make_song_url(artist,title)        
        try:
            lyrics_page = request_lyrics_page(song_url)
        except urllib2.HTTPError, http_error:
            if http_error.code == 404:
                print "LYRICS PAGE NOT FOUND"
                return None
        open(cache_path, 'w').write(lyrics_page)
    
    return open(cache_path).read()
    

def load_song_list(yaml_file):
    return yaml.load_all(yaml_file)

def make_song_url(artist, title):
    return LYRICS_HOST + make_song_path(artist, title)

def make_song_path(artist, title):
    path = "%(artist)s-%(title)s-lyrics" % locals()
    path = re.sub('[^\w]+', '-', path).lower()
    return path + '.html'

def request_lyrics_page(url):
    print 'retrieving: %s' % url
    # to prevent pissing off the lyrics host
    time.sleep(1)
    return urllib2.urlopen(url).read()

if __name__ == '__main__':
    main()