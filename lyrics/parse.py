from BeautifulSoup import BeautifulSoup

def extract_lyrics(song_page):
    soup = BeautifulSoup(song_page, convertEntities=BeautifulSoup.HTML_ENTITIES)
    lyrics = soup('div', id='songlyrics')[0].p.contents
    lyrics = [l for l in lyrics if isinstance(l, basestring)]
    return ''.join(lyrics)

