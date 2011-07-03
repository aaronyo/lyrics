import urllib2
import optparse
import yaml
import re
from pprint import pprint
import time
import os.path

from BeautifulSoup import BeautifulSoup

LYRICS_HOST = 'http://www.lyricstime.com/'
OUT_DIR = os.path.join( os.path.dirname(__file__), '..', 'data', 'scraped')

def main():
    parser = optparse.OptionParser()
    parser.usage = 'usage: %prog SONG_URL|SONG_LIST_FILE ...'
    parser.add_option('-f', '--force', action='store_true', default=False)

    (options, args) = parser.parse_args()
    

    if not args:
        parser.print_help()
        return
    
    lyrics = []
    
    if args[0].endswith('yaml'):
        song_list_file = args[0]
        songs = load_song_list( open(song_list_file) )
        for s in songs:
            out_filename = make_song_filename(s['artist'], s['title'])
            out_path = os.path.join(OUT_DIR, out_filename)
            if os.path.exists(out_path) and not options.force:
                continue
            
            if 'lyrics-url' in s:
                song_url = s['lyrics-url']
            else:
                song_url = make_song_url(s['artist'], s['title'])
                # to prevent pissing off the lyrics host
                
            print 'retrieving: %s' % song_url
            lyrics = scrape_lyrics(song_url)

            if lyrics == 'PAGE NOT FOUND':
                print 'LYRICS PAGE NOT FOUND: %s - %s' % (s['artist'], s['title'])
                continue
            s['lyrics'] = scrape_lyrics(song_url)
            s['url'] = song_url
            yaml.safe_dump(s, open(out_path, 'w'))
            time.sleep(1)
    elif args[0].startswith('http://'):
        song_url = args[0]
        lyrics.append( scrape_lyrics(song_url) )        
    else:
        parser.print_help()
        return
        
#    for l in lyrics:
#        print l
        

def load_song_list(yaml_file):
    return yaml.load_all(yaml_file)

def make_song_url(artist, title):
    path = "%(artist)s-%(title)s-lyrics" % locals()
    path = re.sub('[^\w]+', '-', path).lower()
    path = path + '.html'
    return LYRICS_HOST + path
    
def make_song_filename(artist, title):
    path = "%(artist)s-%(title)s" % locals()
    path = re.sub('[^\w]+', '-', path).lower()
    path = path + '.yaml'
    return path    
    
def scrape_lyrics(url):
    try:
        song_page = urllib2.urlopen(url).read()
    except urllib2.HTTPError, http_error:
        if http_error.code == 404:
            return "PAGE NOT FOUND"
        else:
            raise
            
    soup = BeautifulSoup(song_page, convertEntities=BeautifulSoup.HTML_ENTITIES)
    lyrics = soup('div', id='songlyrics')[0].p.contents
    lyrics = [l for l in lyrics if isinstance(l, basestring)]
    return ''.join(lyrics)

if __name__ == '__main__':
    main()