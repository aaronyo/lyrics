import yaml
import optparse
import re
import os

from collections import defaultdict

_this_file_dir = os.path.dirname( os.path.abspath(__file__) )
DATA_DIR = os.path.join(_this_file_dir, '..', 'data')

def main():
    parser = optparse.OptionParser()
    parser.usage = 'usage: %prog FILE(s) ...'
    (options, args) = parser.parse_args()

    if not args:
        parser.print_help()
        return
        
    f_stop_words = open(os.path.join(DATA_DIR, 'stop_words.txt'))
    stop_words = f_stop_words.read().split('\n')

    print
    for filename in args:
        f = open(filename)
        y = yaml.safe_load(f)
        distrib = word_distribution( y['lyrics'], stop_words )
        print y['title']
        print '-' * len(y['title'])
        print_summary(distrib)
        print
   
def word_distribution( lyrics, stop_words ):
    word_list = re.findall(r"\w+'*\w*", lyrics)

    d = defaultdict(int)
    for word in word_list:
        word = word.lower()
        if word not in stop_words:
            d[word] += 1

    l = [(v, k) for k, v in d.items()]
    sorted_distribution = sorted(l)
    return sorted_distribution    
    
def print_summary( distrib ):
    print 'unique words: %i' % len(distrib)
    print distrib

if __name__ == '__main__':
    main()