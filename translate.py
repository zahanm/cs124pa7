
from __future__ import print_function

import sys
import urllib2

from bs4 import BeautifulSoup

hineng = 'http://hindi-english.org/index.php?input={0}&trans=Translate&direction=AU'
shabdkosh = 'http://www.shabdkosh.com/s?e={0}'

def word_translate(fwords):
  with open(fwords) as f:
    for word in f:
      if len(word.strip()):
        site_stream = urllib2.urlopen(shabdkosh.format(word.strip()))
        html = ''.join([ line for line in site_stream ])
        # print(html)
        soup = BeautifulSoup(html)
        translated = ''
        ol = soup.find('ol', { 'class': 'eirol' })
        if ol:
          # import pdb; pdb.set_trace()
          span = ol.find('span', { 'class': 'en l' })
          if span:
            translated = span.get_text()
        print(word.strip(), '\t', translated)
        print(word.strip(), '\t', translated, file=sys.stderr)

if __name__ == '__main__':
  if len(sys.argv) != 2:
    print('usage: {0} <words_file>'.format(__file__))
    sys.exit(1)
  fname = sys.argv[1]
  word_translate(fname)

