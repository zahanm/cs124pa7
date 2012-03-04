import sys
import os

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

def readTextFromFile(filename):
  textFile = open(filename,'r')
  sentences = [line.strip() for line in textFile]
  textFile.close()
  return sentences


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


def posTagSentences(sentences,filename='sentences'):
  outfile = open(filename,'w')
  for sentence in sentences:
    outfile.write("%s\n" % sentence)
  outfile.close()
  
  runPosTagger(filename)
  return readTextFromFile(filename)


def runPosTagger(filename):
  pass

def transformSentence(s):
  return s
  

if __name__ == '__main__':
  if len(sys.argv) != 3:
    print('usage: {0} <text_file> <dictionary_file>'.format(__file__))
    sys.exit(1)
  textFilename = sys.argv[1]
  dictFilename = sys.argv[2]

  wordDictionary = readDictFromFile(dictFilename)
  sentences = readTextFromFile(textFilename)
  
  sentences = translateWords(sentences,wordDictionary)
  sentences = posTagSentences(sentences)
  sentences = [transformSentence(s) for s in sentences]

  for sentence in sentences:
    print sentence

