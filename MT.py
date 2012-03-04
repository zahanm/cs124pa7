import sys

def readDictFromFile(filename):
  toReturn = dict()
  dictFile = open(filename,'r')
  for i, line in enumerate(dictFile):
    lineParts = line.strip().split("\t")
    if len(lineParts) > 2:
      print "Beware! Weird formatting on line " + str(i) + "!"
    toReturn[lineParts[0]] = lineParts[1]
  dictFile.close()
  return toReturn


def translateWords(sentences,dictionary):
  newSentences = []
  for sentence in sentences:
    newSentence = ""
    for word in sentence.strip().split(" "):
      if word == ',' or word == '-':
        newSentence = newSentence + word
      else:
        newSentence = newSentence + dictionary[word]
      newSentence = newSentence + " "
    newSentences.append(newSentence)
  return newSentences

if __name__ == '__main__':
  if len(sys.argv) != 3:
    print('usage: {0} <text> <dictionary>'.format(__file__))
    sys.exit(1)
  textFilename = sys.argv[1]
  dictFilename = sys.argv[2]
  wordDictionary = readDictFromFile(dictFilename)

  textFile = open(textFilename,'r')
  sentences = [line.strip() for line in textFile]
  textFile.close()

  print translateWords(sentences,wordDictionary)
