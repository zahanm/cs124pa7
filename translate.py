
from __future__ import print_function

import sys
import urillib2

from bs4 import BeautifulSoup

def word_translate(fwords):
  with open(fwords) as f, open('output','w') as out:
    for word in f:
      site_stream = urillib2.urlopen(word.strip())
      html = ''.join([ line for line in site_stream ])
      soup = BeautifulSoup(html)
      tbodies = soup.find_all(class='stil4')
      print(tbodies[1])

if __name__ == '__main__':
  if len(sys.argv) != 2:
    print('usage: {0} <words_file>'.format(__file__))
    sys.exit(1)
  fname = sys.argv[1]
  word_translate(fname)

