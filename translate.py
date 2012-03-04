
from __future__ import print_function

import sys
import urllib2

from bs4 import BeautifulSoup

url = 'http://hindi-english.org/index.php?input={0}&trans=Translate&direction=AU'

def word_translate(fwords):
  with open(fwords) as f:
    for word in f:
      if len(word.strip()):
        site_stream = urllib2.urlopen(url.format(word.strip()))
        html = ''.join([ line for line in site_stream ])
        # print(html)
        soup = BeautifulSoup(html)
        tbodies = soup.find_all('a', { 'class': 'stil4' })
        translated = ''
        if len(tbodies) >= 1:
          translated = tbodies[1].get_text()
        print(word.strip(), '\t', translated)

if __name__ == '__main__':
  if len(sys.argv) != 2:
    print('usage: {0} <words_file>'.format(__file__))
    sys.exit(1)
  fname = sys.argv[1]
  word_translate(fname)

